#!/usr/bin/env python
import sys
import os
import random
import math
import copy
import cv2
import torch

sys.path.append(os.path.join(os.path.dirname(__file__)))

from typing import Tuple
from torch.utils.data import Dataset
from collections import namedtuple
from display import Displayer
from classic_astar import Astar
from custom_exceptions import PathNotFoundException
from custom_types import Node2d, node2onehottensor, nodelist2otensor

PathPlaningDataItem = namedtuple(
    "PathPlaningDataItem", ["name", "map", "start", "goal", "path"]
)


def name_dataitem(map_name: str, item_number: int) -> str:
    """
    Generate a name for a PathPlaningDataItem based on the map name and item number.

    :param map_name: The name of the map.
    :type map_name: str

    :param item_number: The item number.
    :type item_number: int

    :return: The generated name.
    :rtype: str
    """
    parts = map_name.split(".")

    # Check if the string contains a dot
    if len(parts) > 1:
        # Take the part before the dot and add the number
        modified_string = parts[0] + "_" + str(item_number)
    else:
        # If there is no dot, simply add the number to the end of the original string
        modified_string = map_name + "_" + str(item_number)

    return modified_string


def png_to_binary_matrix(
    image_path: str, target_size: int, threshold: int
) -> torch.Tensor:
    """
    Convert a PNG image to a binary matrix.

    :param image_path: The path to the PNG image.
    :type image_path: str

    :param target_size: The target size of the resulting matrix.
    :type target_size: int

    :param threshold: The threshold for binary conversion.
    :type threshold: int

    :return: The binary matrix.
    :rtype: torch.Tensor
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(img, 0, threshold, cv2.THRESH_BINARY_INV)
    resized = cv2.resize(binary_image, (target_size, target_size))
    matrix = torch.tensor(resized)
    return resized


def calculate_distance(point1: Node2d, point2: Node2d) -> float:
    """
    Calculate the Euclidean distance between two Node2d points.

    :param point1: The first Node2d point.
    :type point1: Node2d

    :param point2: The second Node2d point.
    :type point2: Node2d

    :return: The Euclidean distance.
    :rtype: float
    """
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def generate_random_points(
    matrix: torch.Tensor, seed: int = None
) -> Tuple[Node2d, Node2d]:
    """
    Generate random start and goal points on an empty matrix.

    :param matrix: The binary matrix representing the environment.
    :type matrix: torch.Tensor

    :param seed: The random seed for reproducibility (default is None).
    :type seed: int, optional

    :return: A tuple containing the start and goal points.
    :rtype: Tuple[Node2d, Node2d]
    """
    if seed is not None:
        random.seed(seed)

    rows, cols = len(matrix), len(matrix[0])
    min_distance = 0.8 * max(rows, cols)  # Minimum distance is 80% of the matrix size

    # Helper function to get a random point in a specific quarter
    def get_random_point(quarter):
        if quarter == 1:
            return random.randint(0, rows // 2 - 1), random.randint(cols // 2, cols - 1)
        elif quarter == 2:
            return random.randint(0, rows // 2 - 1), random.randint(0, cols // 2 - 1)
        elif quarter == 3:
            return random.randint(rows // 2, rows - 1), random.randint(0, cols // 2 - 1)
        elif quarter == 4:
            return random.randint(rows // 2, rows - 1), random.randint(
                cols // 2, cols - 1
            )

    while True:
        start_quarter = random.randint(1, 4)
        goal_quarter = random.randint(1, 4)

        start_point = Node2d(*get_random_point(start_quarter))
        goal_point = Node2d(*get_random_point(goal_quarter))

        # Check if both points are on empty tiles (value = 0), in different quarters,
        # and the distance is at least 80% of the matrix size
        if (
            matrix[start_point.x][start_point.y] == 0
            and matrix[goal_point.x][goal_point.y] == 0
            and start_quarter != goal_quarter
            and calculate_distance(start_point, goal_point) >= min_distance
        ):
            return start_point, goal_point


class PathPlanningDataset(Dataset):
    def __init__(
        self,
        map_folder_path: str,
        map_size: int,
        problems_on_one_map: int,
        heuristic: callable,
        max_astar_iterations: int,
        randomize_points: bool = False,
    ) -> None:
        """
        Initialize the PathPlanningDataset.

        :param map_folder_path: The path to the folder containing map images.
        :type map_folder_path: str

        :param map_size: The size of the maps (assumed to be square).
        :type map_size: int

        :param problems_on_one_map: The number of problems (start/goal pairs) generated for each map.
        :type problems_on_one_map: int

        :param heuristic: The heuristic function used by the A* algorithm.
        :type heuristic: callable

        :param max_astar_iterations: Maximum number of iterations for the A* algorithm.
        :type max_astar_iterations: int

        :param randomize_points: Flag to indicate whether to randomize start and goal points (default is False).
        :type randomize_points: bool, optional
        """
        super().__init__()
        self.data = []
        self.map_folder_path = map_folder_path
        self.map_size = map_size
        self.problems_on_one_map = problems_on_one_map
        self.heuristic = heuristic
        self.randomize_points = randomize_points
        self.max_astar_iterations_ = max_astar_iterations
        self.displayer = Displayer()
        self.prepare_dataset()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        dataitem = self.data[index]
        return dataitem.map, dataitem.start, dataitem.goal, dataitem.path

    def create_one_item_dataset(self):
        self.data = [self.data[0]]

    def prepare_dataset(self):
        for filename in os.listdir(self.map_folder_path):
            if not filename.endswith(".png"):
                continue
            file_path = os.path.join(self.map_folder_path, filename)

            matrix_original = png_to_binary_matrix(file_path, self.map_size, 1)
            for seed in range(self.problems_on_one_map):
                matrix = copy.copy(matrix_original)
                if not self.randomize_points:
                    start, goal = generate_random_points(matrix, seed)
                else:
                    start, goal = generate_random_points(matrix, seed=None)
                astar = Astar(
                    heuristic=self.heuristic,
                    costmap_weight=1,
                    max_iterations=self.max_astar_iterations_,
                )
                try:
                    solution, _ = astar._run_astar(matrix, start, goal)
                except PathNotFoundException as e:
                    print("Path not found, skipping: ", e)
                    continue
                name = name_dataitem(filename, seed)
                # Convert to PyTorch types
                matrix = torch.from_numpy(matrix)
                start = node2onehottensor(matrix.shape[0], start)
                goal = node2onehottensor(matrix.shape[0], goal)
                solution = nodelist2otensor(matrix.shape[0], solution)
                data_item = PathPlaningDataItem(name, matrix, start, goal, solution)
                self.data.append(data_item)

    def display_dataitem_by_idx(self, idx: int) -> None:
        """
        Display a specific data item using its index.

        :param idx: The index of the data item.
        :type idx: int
        """
        dataitem = self.data[idx]
        dp = Displayer()
        dp.add_matrix(dataitem.map)
        dp.add_goal(dataitem.goal)
        dp.add_start(dataitem.start)
        dp.add_solution(dataitem.path)
        dp.add_title(dataitem.name)
        dp.prepare_plot()
        dp.draw()
