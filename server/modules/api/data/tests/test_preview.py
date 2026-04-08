import csv

from modules.api.data.tests.test_base import DataEndpointTestBase


class PreviewTableTests(DataEndpointTestBase):

    def _write_csv(self, name, headers, rows):
        path = self.tmp / "public" / name
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return path

    def test_preview_csv_returns_all_rows(self):
        self._write_csv("data.csv", ["a", "b"], [[1, 2], [3, 4], [5, 6]])
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/data.csv"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["headers"], ["a", "b"])
        self.assertEqual(len(response.data["rows"]), 3)
        self.assertEqual(response.data["total_rows"], 3)

    def test_preview_csv_with_row_range(self):
        rows = [[str(i), str(i * 10)] for i in range(1, 21)]
        self._write_csv("big.csv", ["id", "value"], rows)
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/big.csv&start_row=5&end_row=10"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["rows"]), 6)
        self.assertEqual(response.data["rows"][0], ["5", "50"])
        self.assertEqual(response.data["rows"][-1], ["10", "100"])
        self.assertEqual(response.data["total_rows"], 20)

    def test_preview_csv_row_range_past_end(self):
        rows = [[str(i)] for i in range(1, 6)]
        self._write_csv("small.csv", ["id"], rows)
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/small.csv&start_row=3&end_row=100"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["rows"]), 3)
        self.assertEqual(response.data["rows"][0], ["3"])
        self.assertEqual(response.data["total_rows"], 5)

    def test_preview_csv_single_row(self):
        rows = [[str(i)] for i in range(1, 11)]
        self._write_csv("ten.csv", ["n"], rows)
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/ten.csv&start_row=7&end_row=7"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["rows"]), 1)
        self.assertEqual(response.data["rows"][0], ["7"])

    def test_preview_headers_returned_with_row_range(self):
        self._write_csv("h.csv", ["col_a", "col_b"], [["x", "y"]])
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/h.csv&start_row=1&end_row=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["headers"], ["col_a", "col_b"])

    def test_preview_missing_path(self):
        response = self.authenticated_client.get("/api/data/preview/table/")
        self.assertEqual(response.status_code, 400)

    def test_preview_nonexistent_file(self):
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/nope.csv"
        )
        self.assertEqual(response.status_code, 404)

    def test_preview_unsupported_extension(self):
        (self.tmp / "public" / "readme.txt").write_text("hello")
        response = self.authenticated_client.get(
            "/api/data/preview/table/?path=public/readme.txt"
        )
        self.assertEqual(response.status_code, 400)
