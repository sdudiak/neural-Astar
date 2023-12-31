import unittest
import torch
from neural_astar.differentiable_astar import DifferentiableAstar


class TestDifferentiableAstar(unittest.TestCase):
    def setUp(self):
        self.differentiable_astar = DifferentiableAstar(
            max_iterations=50000, costmap_weight=1
        )

    def test_select_neighbours(self):
        node = torch.tensor(
            [
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ]
            ],
        )
        neighbor_filter = torch.tensor(
            [[[[1.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0]]]],
        )
        result = self.differentiable_astar._select_neighbours(node, neighbor_filter)
        expected_result = torch.tensor(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )
        self.assertTrue(torch.equal(result, expected_result))

    def test_backtrack_path(self):
        start_batch = torch.tensor(
            [
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
            ]
        )
        goal_batch = torch.tensor(
            [
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
                [
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                ],
            ]
        )
        parents_batch = torch.tensor(
            [
                [
                    8.0,
                    8.0,
                    9.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    9.0,
                    18.0,
                    18.0,
                    8.0,
                    20.0,
                    8.0,
                    8.0,
                    8.0,
                    9.0,
                    18.0,
                    27.0,
                    8.0,
                    29.0,
                    29.0,
                    29.0,
                    30.0,
                    8.0,
                    18.0,
                    8.0,
                    20.0,
                    8.0,
                    38.0,
                    38.0,
                    38.0,
                    8.0,
                    8.0,
                    27.0,
                    27.0,
                    29.0,
                    38.0,
                    8.0,
                    38.0,
                    8.0,
                    8.0,
                    8.0,
                    36.0,
                    37.0,
                    8.0,
                    8.0,
                    38.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                ],
                [
                    8.0,
                    8.0,
                    11.0,
                    11.0,
                    8.0,
                    12.0,
                    8.0,
                    8.0,
                    9.0,
                    18.0,
                    8.0,
                    20.0,
                    20.0,
                    20.0,
                    8.0,
                    8.0,
                    9.0,
                    18.0,
                    11.0,
                    8.0,
                    29.0,
                    8.0,
                    8.0,
                    8.0,
                    17.0,
                    18.0,
                    18.0,
                    20.0,
                    29.0,
                    38.0,
                    8.0,
                    38.0,
                    8.0,
                    8.0,
                    27.0,
                    28.0,
                    8.0,
                    38.0,
                    8.0,
                    38.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    38.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                    8.0,
                ],
            ]
        )

        t = 12
        result = self.differentiable_astar._backtrack_path(
            start_batch, goal_batch, parents_batch, t
        )
        expected_result = torch.tensor(
            [
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ],
            ]
        )
        self.assertTrue(torch.equal(result, expected_result))

    def test_straight_through_softmax_(self):
        val = torch.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=torch.float32)
        result = self.differentiable_astar._straight_through_softmax_(val)
        expected_result = torch.tensor(
            [[[0.0, 0.0], [0.0, 1.0]], [[0.0, 0.0], [0.0, 1.0]]]
        )
        self.assertTrue(torch.equal(result, expected_result))

    def test_forward(self):
        matrix_batch = torch.ones((2, 1, 3, 3))
        start_batch = torch.zeros((2, 1, 3, 3))
        goal_batch = torch.ones((2, 1, 3, 3))
        costmap_batch = torch.ones((2, 1, 3, 3))
        paths_batch, closed_list = self.differentiable_astar.forward(
            matrix_batch, start_batch, goal_batch, costmap_batch
        )
        self.assertIsInstance(paths_batch, torch.Tensor)
        self.assertIsInstance(closed_list, torch.Tensor)
        self.assertEqual(paths_batch.shape, (2, 1, 3, 3))
        self.assertEqual(closed_list.shape, (2, 1, 3, 3))


if __name__ == "__main__":
    unittest.main()
