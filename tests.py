import unittest
from unittest.mock import patch, MagicMock
import requests
from main import get_package_info, parse_dependencies, visualize_dependencies

class TestPackageDependencyAnalyzer(unittest.TestCase):
    def test_get_package_info_success(self):
        # Тест на успешное получение данных о пакете
        with patch.object(requests, 'get', return_value=MagicMock(status_code=200, json=lambda: {"info": {"requires_dist": ["lib1", "lib2"]}})) as mock_get:
            data = get_package_info('test_package')
            self.assertIsNotNone(data)
            self.assertIn("info", data)
            mock_get.assert_called_with("https://pypi.org/pypi/test_package/json")

    def test_get_package_info_failure(self):
        # Тест на обработку ошибки при запросе данных о пакете
        with patch.object(requests, 'get', return_value=MagicMock(status_code=404)) as mock_get:
            with self.assertRaises(Exception) as context:
                get_package_info('bad_package')
            self.assertIn('Не удалось получить информацию о пакете: bad_package', str(context.exception))

    def test_dependencies_parsing_and_visualization(self):
        # Тест на проверку отрисовки графа.
        package_data = {"info": {"requires_dist": ["lib1 (>1.0)", "lib2 (<=2.0)"]}}
        expected_dependencies = ['lib1', 'lib2']
        dependencies = parse_dependencies(package_data)
        self.assertEqual(dependencies, expected_dependencies)

        with patch('main.Digraph') as mock_graph:
            visualize_dependencies('test_package', dependencies)
            mock_graph.assert_called_once()
            mock_graph.return_value.edge.assert_any_call('test_package', 'lib1')
            mock_graph.return_value.edge.assert_any_call('test_package', 'lib2')

if __name__ == '__main__':
    unittest.main()