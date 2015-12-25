# gridlines detector

class GridlineDetector(object):

    STATE_BLACK = 1
    STATE_WHITE = 2
    STATE_GRAY = 3

    def __init__(self, arr):
        self.array = arr

        self.row_gridline_groups = []
        self.col_gridline_groups = []

    @property
    def num_rows(self):
        return len(self.row_gridline_groups) - 1

    @property
    def num_row_gridlines(self):
        return len(self.row_gridline_groups)

    @property
    def num_cols(self):
        return len(self.col_gridline_groups) - 1

    @property
    def num_col_gridlines(self):
        return len(self.col_gridline_groups)


    @staticmethod
    def _pixel_is_white(pixel):
        return pixel > 220

    @staticmethod
    def _pixel_is_black(pixel):
        return pixel < 20

    @staticmethod
    def _pixel_is_gray(pixel):
        return pixel < 200

    @staticmethod
    def _pixel_is(pixel, state):
        if state == GridlineDetector.STATE_BLACK:
            return GridlineDetector._pixel_is_black(pixel)
        if state == GridlineDetector.STATE_WHITE:
            return GridlineDetector._pixel_is_white(pixel)
        if state == GridlineDetector.STATE_GRAY:
            return GridlineDetector._pixel_is_gray(pixel)
        raise Exception("unknown pixel state")

    @staticmethod
    def indices_with_state(arr, state):
        indexes = []
        for i, pixel in enumerate(arr):
            if GridlineDetector._pixel_is(pixel, state):
                indexes.append(i)
        return indexes

    @staticmethod
    def _longest_consecutive_sequence(indices):
        idx = sorted(indices)
        cnt = 1
        max_cnt = 0
        for i in range(1, len(idx)):
            if idx[i] == idx[i-1] + 1:
                cnt += 1
            else:
                max_cnt = max(cnt, max_cnt)
                cnt = 1
        max_cnt = max(cnt, max_cnt)
        return max_cnt

    @staticmethod
    def analyze_line(arr):
        black_idx = GridlineDetector.indices_with_state(arr, GridlineDetector.STATE_BLACK)
        gray_idx = GridlineDetector.indices_with_state(arr, GridlineDetector.STATE_GRAY)

        arr_len = float(len(arr))

        r = {}

        # black
        shade_pct = len(black_idx) / arr_len
        black_idx.sort()
        longest_sequence = GridlineDetector._longest_consecutive_sequence(black_idx)
        r['black'] = dict(shade_pct=shade_pct, longest_sequence=longest_sequence)

        # gray
        shade_pct = len(gray_idx) / arr_len
        black_idx.sort()
        longest_sequence = GridlineDetector._longest_consecutive_sequence(gray_idx)
        r['gray'] = dict(shade_pct=shade_pct, longest_sequence=longest_sequence)

        return r

    def is_gridline(self, arr, number_opposite_lines=None):

        # try black
        data = self.analyze_line(arr)
        if data['black']['shade_pct'] > .5:
            return True

        if data['black']['longest_sequence'] > 10:
            return True

        if data['black']['shade_pct'] > .05:
            squares = .05 * len(arr)
            if 3 * data['black']['longest_sequence'] > squares:
                return True

        # try gray
        if data['gray']['shade_pct'] > .5:
            return True

        if data['gray']['longest_sequence'] > 10:
            return True

        if data['gray']['shade_pct'] > .05:
            squares = .05 * len(arr)
            if 3 * data['gray']['longest_sequence'] > squares:
                return True

        return False

    def is_row_gridline(self, row):
        arr = self.array[row]
        return self.is_gridline(arr)

    def is_col_gridline(self, col):
        arr = self.array[:, col]
        return self.is_gridline(arr)

    @staticmethod
    def _group_lines(indices):
        groups = []
        curr = 0
        curr_group = []
        for gid in indices:
            if gid == curr + 1:
                curr_group.append(gid)
                curr = gid
            else:
                if curr_group:
                    groups.append(curr_group)
                curr = gid
                curr_group = [gid]
        if curr_group:
            groups.append(curr_group)
        return groups

    def detect_gridlines(self):

        rows, cols = self.array.shape
        row_indices = []
        for i in range(rows):
            if self.is_row_gridline(i):
                row_indices.append(i)
        row_gridlines = self._group_lines(row_indices)

        col_indices = []
        for i in range(cols):
            if self.is_col_gridline(i):
                col_indices.append(i)
        col_gridlines = self._group_lines(col_indices)

        self.row_gridline_groups = row_gridlines
        self.col_gridline_groups = col_gridlines

        return row_gridlines, col_gridlines


    def rtop(self, i):
        """row gridline ordinal to pixel location"""
        group = self.row_gridline_groups[i]
        return int(sum(group)/float(len(group)))

    def ctop(self, i):
        """row gridline ordinal to pixel location"""
        group = self.col_gridline_groups[i]
        return int(sum(group)/float(len(group)))

    def ntop(self, row, col):
        """node position to pixel (row, col)"""

        # row position
        row_pos = (self.rtop(row) + self.rtop(row + 1)) / 2
        col_pos = (self.ctop(col) + self.ctop(col + 1)) / 2

        return row_pos, col_pos

    ### Edge Detection

    """
    Assume we have 3 rows and 3 columns, meaning
    4 row gridlines and 4 column gridlines

    Row spaces
    |----|----|    |

    In this example: [True, True, False]

    Col Spaces

    -
    |
    |
    |
    -



    -
    |
    |
    |
    -

    In this example, [True, False, True]

    """

    # is row edge
    def is_row_edge(self, row_gridline, position):
        col_from = position
        col_to = position + 1

        row_pixels = self.row_gridline_groups[row_gridline]

        pixels = []
        for r in row_pixels:
            for c in range(self.ctop(col_from), self.ctop(col_to)):
                pixels.append(self.array[r][c])

        is_gray = [self._pixel_is(p, self.STATE_GRAY) for p in pixels]
        cnt_gray = sum(filter(None, is_gray))
        return cnt_gray / float(len(pixels)) > .8

    def is_col_edge(self, col_gridline, position):
        row_from = position
        row_to = position + 1

        col_pixels = self.col_gridline_groups[col_gridline]

        pixels = []
        for r in range(self.rtop(row_from), self.rtop(row_to)):
            for c in col_pixels:
                pixels.append(self.array[r][c])

        is_gray = [self._pixel_is(p, self.STATE_GRAY) for p in pixels]
        cnt_gray = sum(filter(None, is_gray))
        return cnt_gray / float(len(pixels)) > .8


    def is_move_valid(self, row, col, move):
        if move == "left":
            return not self.is_col_edge(col, row)
        if move == "right":
            return not self.is_col_edge(col + 1, row)
        if move == "up":
            return not self.is_row_edge(row, col)
        if move == "down":
            return not self.is_row_edge(row + 1, col)



