import ezdxf
import numpy as np


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

    def _create_pillar(self, x, y):
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

    def _generate_coordinates(self):
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

    def _place_pillars(self):
        """
        Places multiple pillars on the drawing based on the generated coordinates.
        """
        coordinates = self._generate_coordinates()
        for coord in coordinates:
            self._create_pillar(*coord)

    def _horizontal_beam(self, x1, x2, y1, y2):
        """
        Adjusts the coordinates for horizontal beams.

        Parameters:
            x1, x2: float - Start and end x-coordinates.
            y1, y2: float - Start and end y-coordinates.

        Returns:
            Tuple[float, float, float, float] - Adjusted coordinates (x1up, x1down, x2up, x2down).
        """
        half_bv = self.bv / 2
        half_pillars_dimension = self.pillar_dimension / 2

        if self.bv <= self.pillar_dimension:
            x1 += half_pillars_dimension
            x2 -= half_pillars_dimension
            x1up = x1down = x1
            x2up = x2down = x2
        else:
            x2up = x2down = x2
            x1up = x1down = x1
            if x1 == 0:
                x1up += half_bv
                x1down += half_bv
                if y1 == 0:
                    x1down -= 2 * half_bv
                elif y1 == self.divisions_y * self.span_y:
                    x1up -= 2 * half_bv
            elif x2 == self.divisions_x * self.span_x:
                x2up -= half_bv
                x2down -= half_bv
                if y1 == 0:
                    x2down += 2 * half_bv
                elif y1 == self.divisions_y * self.span_y:
                    x2up += 2 * half_bv
        return x1up, x1down, x2up, x2down

    def _vertical_beam(self, x1, x2, y1, y2):
        """
        Adjusts the coordinates for vertical beams.

        Parameters:
            x1, x2: float - Start and end x-coordinates.
            y1, y2: float - Start and end y-coordinates.

        Returns:
            Tuple[float, float, float, float] - Adjusted coordinates (y1left, y1right, y2left, y2right).
        """
        half_bv = self.bv / 2
        half_pillars_dimension = self.pillar_dimension / 2
        if self.bv <= self.pillar_dimension:
            y1 += half_pillars_dimension
            y2 -= half_pillars_dimension
            y1left = y1right = y1
            y2left = y2right = y2
        else:
            y1left = y1right = y1
            y2left = y2right = y2
            if y1 == 0:
                y1left += half_bv
                y1right += half_bv
                if x1 == 0:
                    y1left -= 2 * half_bv
                elif x2 == self.divisions_x * self.span_x:
                    y1right -= 2 * half_bv
            elif y2 == self.divisions_y * self.span_y:
                y2left -= half_bv
                y2right -= half_bv
                if x1 == 0:
                    y2left += 2 * half_bv
                elif x2 == self.divisions_x * self.span_x:
                    y2right += 2 * half_bv
        return y1left, y1right, y2left, y2right

    def _add_primary_beams(self):
        """
        Adds primary beams to the drawing, connecting pillars along the specified direction.
        """
        coordinates = self._generate_coordinates()
        half_bv = self.bv / 2
        axis = 1 if self.dl == 0 else 0
        coordinates.sort(key=lambda c: c[axis])

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
                    x1up, x1down, x2up, x2down = self._horizontal_beam(x1, x2, y1, y2)
                    self.msp.add_line(
                        (x1down, y1 - half_bv),
                        (x2down, y2 - half_bv),
                        dxfattribs={"color": 3},
                    )
                    self.msp.add_line(
                        (x1up, y1 + half_bv),
                        (x2up, y2 + half_bv),
                        dxfattribs={"color": 3},
                    )
                else:  # Vertical beams
                    y1left, y1right, y2left, y2right = self._vertical_beam(
                        x1, x2, y1, y2
                    )
                    self.msp.add_line(
                        (x1 - half_bv, y1left),
                        (x2 - half_bv, y2left),
                        dxfattribs={"color": 3},
                    )
                    self.msp.add_line(
                        (x1 + half_bv, y1right),
                        (x2 + half_bv, y2right),
                        dxfattribs={"color": 3},
                    )

    def _add_secondary_beams(self):
        """
        Adds secondary beams to the drawing in the first and last rows/columns of pillars.
        """
        coordinates = self._generate_coordinates()
        half_bv = self.bv / 2
        axis = 0 if self.dl == 0 else 1
        coordinates.sort(key=lambda c: (c[1 - axis], c[axis]))

        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        groups = list(grouped.values())
        target_groups = [groups[0], groups[-1]]

        for group in target_groups:
            group.sort(key=lambda c: c[axis])
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                if self.dl == 0:  # Horizontal secondary beams
                    x1up, x1down, x2up, x2down = self._horizontal_beam(x1, x2, y1, y2)
                    self.msp.add_line(
                        (x1down, y1 - half_bv),
                        (x2down, y2 - half_bv),
                        dxfattribs={"color": 3},
                    )
                    self.msp.add_line(
                        (x1up, y1 + half_bv),
                        (x2up, y2 + half_bv),
                        dxfattribs={"color": 3},
                    )
                else:  # Vertical secondary beams
                    y1left, y1right, y2left, y2right = self._vertical_beam(
                        x1, x2, y1, y2
                    )

                    self.msp.add_line(
                        (x1 - half_bv, y1left),
                        (x2 - half_bv, y2left),
                        dxfattribs={"color": 3},
                    )
                    self.msp.add_line(
                        (x1 + half_bv, y1right),
                        (x2 + half_bv, y2right),
                        dxfattribs={"color": 3},
                    )

    def _add_dimension_lines(self):
        """
        Adds external dimension lines marking the axes of the pillars.

        - Horizontal dimensions are added above and below the topmost and bottommost rows of pillars.
        - Vertical dimensions are added to the left and right of the leftmost and rightmost columns of pillars.
        """
        coordinates = self._generate_coordinates()
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
                            "insert": (x + self.span_x * 0.45, y_offset + 30),
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
                            "insert": (x_offset - 30, y + self.span_y * 0.45),
                            "color": 2,  # Yellow
                        },  # Vertical alignment
                    )

    def _add_pillar_labels(self):
        """
        Adds labels with pillar names and dimensions at the center of each pillar.

        The pillars will be numbered from the topmost row, starting from the rightmost column,
        moving to the left, then to the next row below.
        """
        coordinates = self._generate_coordinates()
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
                        x + self.bv / 2 + 5,
                        y - self.bv + 5,
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
                        x + self.bv / 2 + 5,
                        y - self.bv - 15,
                    ),  # Position below the center of the pillar
                    "color": 1,  # Black color for the dimension
                },
            )

            pillar_number += 1  # Increment the pillar number for the next pillar

    def _label_beams(self):
        if self.dl:
            self._label_primary_beams()
            self._label_secondary_beams()
        else:
            self._label_secondary_beams()
            self._label_primary_beams()

    def _label_primary_beams(self):
        """Adds labels to the beams with numbering and orientation."""
        coordinates = self._generate_coordinates()
        axis = 1 if self.dl == 0 else 0
        if self.dl:
            self.label_count = 1  # Start numbering from V1
            coordinates.sort(key=lambda coord: (-coord[1], coord[0]))
        else:
            coordinates.sort(key=lambda coord: (coord[0], -coord[1]))
        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        for group in grouped.values():
            group.sort(key=lambda c: c[axis], reverse=(not self.dl))
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2

                label_text = f"V{self.label_count} {self.bv}x{self.hv}"
                if self.dl == 0:
                    rotation = 90
                    y = y_center - self.span_y * 0.1
                    x = x2 - self.bv / 2
                else:
                    y = y2 + self.bv / 2
                    x = x_center - self.span_x * 0.1
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
                self.label_count += 1

    def _label_secondary_beams(self):
        """Adds labels to the secondary beams with numbering and orientation."""
        coordinates = self._generate_coordinates()
        half_bv = self.bv / 2
        axis = 0 if self.dl == 0 else 1
        # Ordena as coordenadas com base no critério de 'dl'
        if self.dl == 0:  # Para vigas horizontais
            # Ordena primeiro por Y (de cima para baixo) e depois por X (da esquerda para direita)
            coordinates.sort(key=lambda c: (c[0], -c[1]))
        else:  # Para vigas verticais
            # Ordena primeiro por X (da esquerda para direita) e depois por Y (de cima para baixo)
            coordinates.sort(key=lambda c: (-c[1], c[0]))

        grouped = {}
        for coord in coordinates:
            key = coord[1 - axis]
            grouped.setdefault(key, []).append(coord)

        groups = list(grouped.values())
        target_groups = [
            groups[0],
            groups[-1],
        ]  # Apenas as primeiras e últimas linhas/colunas
        if self.dl == 0:
            self.label_count = 1  # Começar a numeração de S1

        for group in target_groups:
            group.sort(key=lambda c: c[axis], reverse=(self.dl))
            for i in range(len(group) - 1):
                x1, y1 = group[i]
                x2, y2 = group[i + 1]
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2

                label_text = f"V{self.label_count} {self.bv}x{self.hv}"
                if self.dl == 0:  # Para vigas horizontais secundárias
                    rotation = 0
                    y = y2 + half_bv
                    x = x_center - self.span_x * 0.1
                else:  # Para vigas verticais secundárias
                    y = y_center - self.span_y * 0.1
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
                self.label_count += 1

    def generate_drawing(self):
        """
        Generates the structural drawing by sequentially executing key steps.

        This method compiles the drawing by performing the following operations:
        1. Places the pillars in their designated locations.
        2. Adds the primary beams to the drawing.
        3. Adds the secondary beams to the drawing.
        4. Inserts external dimension lines for better understanding of the layout.
        5. Labels the pillars with unique identifiers for clarity.
        6. Labels the primary beams with appropriate annotations.
        7. Labels the secondary beams with appropriate annotations.
        8. Saves the generated drawing to a predefined file format.

        This function ensures a comprehensive and labeled structural drawing
        for further use or presentation.

        Returns:
            None
        """
        self._place_pillars()
        self._add_primary_beams()
        self._add_secondary_beams()
        self._add_dimension_lines()  # Adiciona cotagem externa
        self._add_pillar_labels()  # Adiciona rótulos aos pilares
        self._label_beams()  # Adiciona rótulos aos pilares

        self._save()

    def _save(self):
        """
        Saves the DXF file with the specified name.
        """
        self.doc.saveas(self.filename)
        print(f"File '{self.filename}' saved successfully!")


class TBeamDrawingDWG:
    def __init__(self, bw, hl, hv, Na, Nb, NPT, file_name="viga_T_invertido.dxf"):
        """
        Inicializa a classe com as dimensões da viga T invertido e o nome do arquivo DXF.

        :param bw: Largura da alma (cm)
        :param hl: Altura da laje (cm)
        :param hv: Altura inferior da viga (cm)
        :param file_name: Nome do arquivo DXF (default: 'viga_T_invertido.dxf')
        :param Na: Quantidade de cabos na primeira camada
        :param Nb: Quantidade de cabos na segunda camada
        """
        self.bw = bw
        self.hl = hl
        self.hv = hv
        self.base = 15 + bw + 15  # largura total da base da viga em T invertido
        self.height = hv + (hl - 5)  # altura total da viga
        self.Na = Na
        self.Nb = Nb
        self.NPT = NPT
        self.file_name = file_name  # Nome do arquivo DXF a ser gerado

    def generate_drawing(self):
        """
        Cria o arquivo DXF com a viga T invertido e as cotas.
        """
        doc = self._create_dxf_document()
        msp = doc.modelspace()

        # Criando a polilinha da viga
        self._add_viga_polyline(msp)

        # Adicionando cabos de protensao
        self._add_pretension_cables(msp)

        self._add_passive_reinforcement(msp)

        # Adicionando as cotas
        self._add_cotas(msp)

        # Salvando o arquivo DXF
        self._save(doc)

    def _save(self, doc):
        """
        Saves the DXF file with the specified name.
        """
        doc.saveas(self.file_name)
        print(f"File '{self.file_name}' saved successfully!")

    def _create_dxf_document(self):
        """
        Cria e retorna um novo documento DXF.
        """
        doc = ezdxf.new("R2000")
        doc.layers.new(name="Viga_T", dxfattribs={"color": 7})  # Cor 7 (branco)
        return doc

    def _add_viga_polyline(self, msp):
        """
        Adiciona a polilinha que define a geometria da viga T invertido no desenho.

        :param msp: ModelSpace do documento DXF
        """
        points = np.array(
            [
                [0, 0],  # ponto (0,0)
                [self.base, 0],  # ponto (30+bw, 0)
                [self.base, self.hv],  # ponto (30+bw, hv)
                [15 + self.bw, self.hv],  # ponto (15+bw, hv)
                [15 + self.bw, self.hv + self.hl - 5],  # ponto (15+bw, hv+hl-5)
                [15, self.hv + self.hl - 5],  # ponto (15, hv+hl-5)
                [15, self.hv],  # ponto (15, hv)
                [0, self.hv],  # ponto (0, hv)
            ]
        )
        msp.add_lwpolyline(points, close=True)  # Fechando o polígono

    def _add_cotas(self, msp):
        """
        Adiciona as cotas horizontais e verticais no desenho DXF.

        :param msp: ModelSpace do documento DXF
        """
        self._add_cota_bw(msp)
        self._add_cota_base(msp)
        self._add_cota_hv(msp)
        self._add_cota_hl(msp)

    def _add_cota_bw(self, msp):
        """
        Adiciona a cota da largura da alma (Bw).

        :param msp: ModelSpace do documento DXF
        """
        y_offset = self.height + 10  # Posição vertical para a cota Bw
        self._add_dimension(msp, (15, y_offset), (15 + self.bw, y_offset), self.bw, 0)

    def _add_cota_base(self, msp):
        """
        Adiciona a cota da largura da base.

        :param msp: ModelSpace do documento DXF
        """
        y_offset = -10  # Posição vertical para a cota da base
        self._add_dimension(msp, (0, y_offset), (self.base, y_offset), self.base, 0)

    def _add_cota_hv(self, msp):
        """
        Adiciona a cota da altura inferior da viga (Hv).

        :param msp: ModelSpace do documento DXF
        """
        x_offset = self.base + 10  # Posição horizontal para a cota Hv
        self._add_dimension(msp, (x_offset, 0), (x_offset, self.hv), self.hv, 1)

    def _add_cota_hl(self, msp):
        """
        Adiciona a cota da altura da laje (Hl - 5).

        :param msp: ModelSpace do documento DXF
        """
        x_offset = self.base + 10  # Posição horizontal para a cota Hl
        self._add_dimension(
            msp, (x_offset, self.hv), (x_offset, self.height), (self.hl - 5), 1
        )

    def _add_dimension(self, msp, start_point, end_point, value, sentido):
        """
        Adiciona uma linha de cota no desenho.

        :param msp: ModelSpace do documento DXF
        :param start_point: Ponto inicial da linha de cota
        :param end_point: Ponto final da linha de cota
        :param text_position: Posição do texto da cota
        :param value: Valor da cota a ser exibido
        """
        x_mean = (start_point[0] + end_point[0]) / 2
        y_mean = (start_point[1] + end_point[1]) / 2
        if sentido:
            y = y_mean * 0.95
            x = start_point[0]
            rotation = 90
            msp.add_line(
                (start_point[0] - 5, start_point[1]),
                (start_point[0] + 5, start_point[1]),
                dxfattribs={"color": 2},
            )
            msp.add_line(
                (end_point[0] - 5, end_point[1]),
                (end_point[0] + 5, end_point[1]),
                dxfattribs={"color": 2},
            )
        else:
            x = x_mean * 0.95
            y = start_point[1]
            rotation = 0
            # Adiciona os marcadores de cota (ticks)
            msp.add_line(
                (start_point[0], start_point[1] - 5),
                (start_point[0], start_point[1] + 5),
                dxfattribs={"color": 2},
            )
            msp.add_line(
                (end_point[0], end_point[1] - 5),
                (end_point[0], end_point[1] + 5),
                dxfattribs={"color": 2},
            )

        text_position = (x, y)

        # Adiciona a linha de cota
        msp.add_line(start_point, end_point, dxfattribs={"color": 2})

        # Adiciona o texto da cota
        msp.add_text(
            str(value),
            dxfattribs={
                "height": 2.5,
                "rotation": rotation,
                "insert": text_position,
                "halign": 0.5,
                "valign": 0.5,
                "color": 2,  # Yellow
            },
        )

    def _add_pretension_cables(self, msp):
        """
        Adiciona a representação dos cabos de protensão na base da viga em duas camadas.

        :param msp: ModelSpace do documento DXF
        """
        # Primeira camada
        if self.Na > 0:
            self._add_cable_layer(msp, self.Na, cable_height=5, layer_name="Pretensao1")

        # Segunda camada
        if self.Nb > 0:
            self._add_cable_layer(
                msp, self.Nb, cable_height=10, layer_name="Pretensao2"
            )

    def _add_passive_reinforcement(self, msp):
        """
        Adiciona a representação da armadura passiva.

        :param msp: ModelSpace do documento DXF
        """
        # Primeira camada
        if self.NPT > 0:
            cable_height = self.height - 5
            self._add_reinforced_layer(
                msp, self.NPT, cable_height=cable_height, layer_name="Pretensao1"
            )

    def _add_reinforced_layer(self, msp, num_cables, cable_height, layer_name):
        """
        Adiciona uma camada de cabos de protensão no desenho DXF.

        :param msp: ModelSpace do documento DXF
        :param num_cables: Número de cabos na camada
        :param cable_height: Altura da camada acima da base
        :param layer_name: Nome do layer para os cabos
        """
        distance = self.bw / (num_cables + 1)  # Distância entre os cabos
        for i in range(1, num_cables + 1):
            x_position = distance * i + 15
            msp.add_circle(
                (x_position, cable_height),  # Posição da bolinha
                radius=1,  # Tamanho da bolinha (cabo de protensão)
                dxfattribs={"layer": layer_name, "color": 2},  # Cor vermelha
            )

    def _add_cable_layer(self, msp, num_cables, cable_height, layer_name):
        """
        Adiciona uma camada de cabos de protensão no desenho DXF.

        :param msp: ModelSpace do documento DXF
        :param num_cables: Número de cabos na camada
        :param cable_height: Altura da camada acima da base
        :param layer_name: Nome do layer para os cabos
        """
        distance = self.base / (num_cables + 1)  # Distância entre os cabos
        for i in range(1, num_cables + 1):
            x_position = distance * i
            msp.add_circle(
                (x_position, cable_height),  # Posição da bolinha
                radius=0.5,  # Tamanho da bolinha (cabo de protensão)
                dxfattribs={"layer": layer_name, "color": 1},  # Cor vermelha
            )


# Example Usage
if __name__ == "__main__":
    # Exemplo de uso
    beam_orientation = (1,)
    pillar_size = 50
    beam_width = 60  # Largura da alma (exemplo)
    beam_height = 20  # Altura inferior da viga (exemplo)
    slab_height = 20  # Altura da laje (exemplo)
    # Número de cabos por camada
    Na = 10  # Número de cabos na primeira camada
    Nb = 4  # Número de cabos na segunda camada
    NPT = 5
    span_x = 775
    span_y = 800
    num_divisions_x = 6
    num_divisions_y = 6
    plant = PavementDesign(
        filename="planta_com_labels.dxf",
        beam_orientation=0,
        beam_width=beam_width,
        beam_height=beam_height,
        pillar_size=pillar_size,
        span_x=span_x,
        span_y=span_y,
        num_divisions_x=num_divisions_x,
        num_divisions_y=num_divisions_y,
    )

    plant.generate_drawing()
    viga = TBeamDrawingDWG(beam_width, slab_height, beam_height, Na, Nb, NPT)
    viga.generate_drawing()
