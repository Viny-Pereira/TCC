import ezdxf


class PavementDesign:
    def __init__(
        self,
        filename="plant.dxf",
        beam_orientation=0,
        beam_width=40,
        beam_height=60,
        pillar_size=50,
        span_x=800,
        span_y=800,
        num_divisions_x=4,
        num_divisions_y=3,
    ):
        """
        Initializes the DXF document, modelspace, and structural design parameters for the pavement.

        :param filename: Name of the DXF file to be created.
        :param beam_orientation: Direction of beams (0 for X-axis, 1 for Y-axis).
        :param beam_width: Width of the beams.
        :param pillar_size: Size of the square pillars.
        :param span_x: Distance between pillars along the X-axis.
        :param span_y: Distance between pillars along the Y-axis.
        :param num_divisions_x: Number of divisions along the X-axis for pillar placement.
        :param num_divisions_y: Number of divisions along the Y-axis for pillar placement.
        """
        if beam_width <= 0:
            raise ValueError("Beam width (BV) must be positive.")
        if pillar_size <= 0:
            raise ValueError("Pillar dimension must be positive.")
        if span_x <= 0 or span_y <= 0:
            raise ValueError("Span values must be positive.")
        if num_divisions_x < 1 or num_divisions_y < 1:
            raise ValueError("Number of divisions must be at least 1.")

        self.doc = ezdxf.new()
        self.msp = self.doc.modelspace()
        self.filename = filename
        self.dl = beam_orientation
        self.bv = beam_width
        self.hv = beam_height
        self.pillar_dimension = pillar_size
        self.span_x = span_x
        self.span_y = span_y
        self.divisions_x = num_divisions_x
        self.divisions_y = num_divisions_y

    def create_pillar(self, x, y):
        """
        Creates a square pillar based on the center coordinates and side dimension.

        :param x: X-coordinate of the pillar's center
        :param y: Y-coordinate of the pillar's center
        """
        half_dim = self.pillar_dimension / 2
        points = [
            (x - half_dim, y - half_dim),
            (x + half_dim, y - half_dim),
            (x + half_dim, y + half_dim),
            (x - half_dim, y + half_dim),
            (x - half_dim, y - half_dim),  # Close the square
        ]
        self.msp.add_lwpolyline(points, close=True, dxfattribs={"color": 1})

    def generate_coordinates(self):
        """
        Generates coordinates for pillars based on the design parameters.

        :return: List of tuples with coordinates [(x1, y1), (x2, y2), ...]
        """
        coordinates = []
        for i in range(self.divisions_x + 1):  # Add 1 for n+1 pillars
            for j in range(self.divisions_y + 1):  # Add 1 for n+1 pillars
                x = i * self.span_x
                y = j * self.span_y
                coordinates.append((x, y))
        return coordinates

    def place_pillars(self):
        """
        Places multiple pillars on the drawing based on the generated coordinates.
        """
        coordinates = self.generate_coordinates()
        for coord in coordinates:
            self.create_pillar(*coord)

    def add_primary_beams(self):
        """
        Adds primary beams to the drawing, connecting pillars along the specified direction.
        """
        coordinates = self.generate_coordinates()
        half_bv = self.bv / 2
        axis = 1 if self.dl == 0 else 0
        coordinates.sort(key=lambda c: c[axis])
        half_pillars_dimension = self.pillar_dimension / 2

        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        for group in grouped.values():
            group.sort(key=lambda c: c[axis])
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                if self.dl == 1:  # Horizontal beams
                    x1 += half_pillars_dimension
                    x2 -= half_pillars_dimension
                    self.msp.add_line(
                        (x1, y1 - half_bv), (x2, y2 - half_bv), dxfattribs={"color": 3}
                    )
                    self.msp.add_line(
                        (x1, y1 + half_bv), (x2, y2 + half_bv), dxfattribs={"color": 3}
                    )
                else:  # Vertical beams
                    y1 += half_pillars_dimension
                    y2 -= half_pillars_dimension
                    self.msp.add_line(
                        (x1 - half_bv, y1), (x2 - half_bv, y2), dxfattribs={"color": 3}
                    )
                    self.msp.add_line(
                        (x1 + half_bv, y1), (x2 + half_bv, y2), dxfattribs={"color": 3}
                    )

    def add_secondary_beams(self):
        """
        Adds secondary beams to the drawing in the first and last rows/columns of pillars.
        """
        coordinates = self.generate_coordinates()
        half_bv = self.bv / 2
        axis = 0 if self.dl == 0 else 1
        coordinates.sort(key=lambda c: (c[1 - axis], c[axis]))

        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        groups = list(grouped.values())
        target_groups = [groups[0], groups[-1]]
        half_pillars_dimension = self.pillar_dimension / 2

        for group in target_groups:
            group.sort(key=lambda c: c[axis])
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                if self.dl == 0:  # Horizontal secondary beams
                    x1 += half_pillars_dimension
                    x2 -= half_pillars_dimension
                    self.msp.add_line(
                        (x1, y1 - half_bv), (x2, y2 - half_bv), dxfattribs={"color": 3}
                    )
                    self.msp.add_line(
                        (x1, y1 + half_bv), (x2, y2 + half_bv), dxfattribs={"color": 3}
                    )
                else:  # Vertical secondary beams
                    y1 += half_pillars_dimension
                    y2 -= half_pillars_dimension
                    self.msp.add_line(
                        (x1 - half_bv, y1), (x2 - half_bv, y2), dxfattribs={"color": 3}
                    )
                    self.msp.add_line(
                        (x1 + half_bv, y1), (x2 + half_bv, y2), dxfattribs={"color": 3}
                    )

    def add_dimension_lines(self):
        """
        Adds external dimension lines marking the axes of the pillars.

        - Horizontal dimensions are added above and below the topmost and bottommost rows of pillars.
        - Vertical dimensions are added to the left and right of the leftmost and rightmost columns of pillars.
        """
        coordinates = self.generate_coordinates()
        if not coordinates:
            return  # No coordinates to process

        # Determine the extents
        min_x = min(coord[0] for coord in coordinates)
        max_x = max(coord[0] for coord in coordinates)
        min_y = min(coord[1] for coord in coordinates)
        max_y = max(coord[1] for coord in coordinates)

        # Horizontal dimension lines
        for y_offset in [-self.span_y / 2, max_y + self.span_y / 2]:
            line_points = [(min_x, y_offset), (max_x, y_offset)]
            self.msp.add_line(line_points[0], line_points[1], dxfattribs={"color": 2})
            for x in sorted(set(coord[0] for coord in coordinates)):
                self.msp.add_line(
                    (x, y_offset - 20), (x, y_offset + 20), dxfattribs={"color": 2}
                )  # Tick marks
                if x != coordinates[-1][0]:
                    self.msp.add_text(
                        str(self.span_x),
                        dxfattribs={
                            "height": 40,
                            "halign": 0.5,
                            "valign": 0.5,
                            "insert": (x + self.span_x / 2, y_offset + 30),
                            "color": 2,  # Yellow
                        },  # Horizontal alignment
                    )

        # Vertical dimension lines
        for x_offset in [-self.span_x / 2, max_x + self.span_x / 2]:
            line_points = [(x_offset, min_y), (x_offset, max_y)]
            self.msp.add_line(line_points[0], line_points[1], dxfattribs={"color": 2})
            for y in sorted(set(coord[1] for coord in coordinates)):
                self.msp.add_line(
                    (x_offset - 20, y), (x_offset + 20, y), dxfattribs={"color": 2}
                )  # Tick marks
                if y != coordinates[-1][1]:
                    self.msp.add_text(
                        str(self.span_y),
                        dxfattribs={
                            "height": 40,
                            "halign": 0.5,
                            "valign": 0.5,
                            "rotation": 90,
                            "insert": (x_offset - 30, y + self.span_y / 2),
                            "color": 2,  # Yellow
                        },  # Vertical alignment
                    )

    def add_pillar_labels(self):
        """
        Adds labels with pillar names and dimensions at the center of each pillar.

        The pillars will be numbered from the topmost row, starting from the rightmost column,
        moving to the left, then to the next row below.
        """
        coordinates = self.generate_coordinates()
        # Organize coordinates by rows (same y-value)
        coordinates.sort(
            key=lambda coord: (-coord[1], coord[0])
        )  # Sort by Y descending, then X descending
        pillar_number = 1  # Start numbering from P1

        for coord in coordinates:
            x, y = coord
            label = f"P{pillar_number}"  # Label for the pillar, e.g., P1, P2, etc.
            dimension = f"{self.pillar_dimension}x{self.pillar_dimension}"  # Dimension of the pillar

            # Add the label (P1, P2, etc.)
            self.msp.add_text(
                label,
                dxfattribs={
                    "height": 20,
                    "halign": 0.5,  # Horizontal alignment to center
                    "valign": 0.5,  # Vertical alignment to center
                    "insert": (
                        x + self.pillar_dimension / 2 + 5,
                        y - self.pillar_dimension / 2 - 20,
                    ),  # Position above the center of the pillar
                    "color": 1,  # Black color for the label
                },
            )

            # Add the dimension (e.g., 50x50)
            self.msp.add_text(
                dimension,
                dxfattribs={
                    "height": 15,
                    "halign": 0.5,  # Horizontal alignment to center
                    "valign": 0.5,  # Vertical alignment to center
                    "insert": (
                        x + self.pillar_dimension / 2 + 5,
                        y - self.pillar_dimension / 2 - 40,
                    ),  # Position below the center of the pillar
                    "color": 1,  # Black color for the dimension
                },
            )

            pillar_number += 1  # Increment the pillar number for the next pillar

    def label_beams(self):
        """Adds labels to the beams with numbering and orientation."""
        coordinates = self.generate_coordinates()
        axis = 1 if self.dl == 0 else 0
        coordinates.sort(key=lambda c: c[axis])

        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        label_count = 1  # Start numbering from V1
        for group in grouped.values():
            group.sort(key=lambda c: c[axis])
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2

                label_text = f"{self.bv}x{self.hv}"
                if self.dl == 0:
                    rotation = 90
                    y = y_center
                    x = x2 - self.bv / 2
                else:
                    y = y2 + self.bv / 2
                    x = x_center
                    rotation = 0

                self.msp.add_text(
                    label_text,
                    dxfattribs={
                        "height": 20,
                        "halign": 0.5,
                        "valign": 0.5,
                        "insert": (x, y),
                        "color": 3,  # Cyan
                        "rotation": rotation,
                    },
                )
                label_count += 1

    def label_secondary_beams(self):
        """Adds labels to the secondary beams with numbering and orientation."""
        coordinates = self.generate_coordinates()
        half_bv = self.bv / 2
        axis = 0 if self.dl == 0 else 1
        coordinates.sort(key=lambda c: (c[1 - axis], c[axis]))

        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        groups = list(grouped.values())
        target_groups = [
            groups[0],
            groups[-1],
        ]  # Apenas as primeiras e últimas linhas/colunas
        label_count = 1  # Começar a numeração de S1

        for group in target_groups:
            group.sort(key=lambda c: c[axis])
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2

                label_text = f"{self.bv}x{self.hv}"
                if self.dl == 0:  # Para vigas horizontais secundárias
                    rotation = 0
                    y = y2 + half_bv
                    x = x_center
                else:  # Para vigas verticais secundárias
                    y = y_center
                    x = x2 - half_bv
                    rotation = 90

                # Adicionando o rótulo da viga
                self.msp.add_text(
                    label_text,
                    dxfattribs={
                        "height": 20,
                        "halign": 0.5,
                        "valign": 0.5,
                        "insert": (x, y),
                        "color": 3,  # Ciano
                        "rotation": rotation,
                    },
                )
                label_count += 1

    def save(self):
        """
        Saves the DXF file with the specified name.
        """
        self.doc.saveas(self.filename)
        print(f"File '{self.filename}' saved successfully!")


# Example Usage
if __name__ == "__main__":
    plant = PavementDesign(
        filename="planta_com_labels.dxf",
        beam_orientation=1,
        beam_width=40,
        beam_height=60,
        pillar_size=50,
        span_x=775,
        span_y=900,
        num_divisions_x=4,
        num_divisions_y=3,
    )
    plant.place_pillars()
    plant.add_primary_beams()
    plant.add_secondary_beams()
    plant.add_dimension_lines()  # Adiciona cotagem externa
    plant.add_pillar_labels()  # Adiciona rótulos aos pilares
    plant.label_beams()  # Adiciona rótulos aos pilares
    plant.label_secondary_beams()

    plant.save()
