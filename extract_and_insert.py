from utils import *
import utils

# PEGA OS DADOS DA PEÇA ATUAL E CHAMA A FUNCAO DE INSERIR INSTANCIA
# VERSAO ANTIGA PQ DEU MERDA NA ATUAL
def insert_data(onto, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterando pelas linhas
    for line in lines:
        #print(f'LINHA: {line}')
        # Verificando o tipo de linha

        if line.startswith('Part name'):
            name = re.compile(r'Part name: (.+)').match(line).group(1)
            name_instance = onto.Part_Name(f'{name}')
            name_instance.hasName.append(name)

        elif line.startswith('web'):
            match = utils.pattern_web.match(line)
            if match:
                web_id = int(match.group(1))
                web_position_x = float(match.group(2))
                web_position_y = float(match.group(3))
                web_position_z = float(match.group(4))

                web_normal_x = float(match.group(5))
                web_normal_y = float(match.group(6))
                web_normal_z = float(match.group(7))

                # Inserindo na ontologia
                web_instance = onto.Web(f'{name}_{web_id}')
                web_instance.hasID.append(web_id)
                web_instance.hasName.append(name)

                web_instance.hasPosition_Point_X.append(web_position_x)
                web_instance.hasPosition_Point_Y.append(web_position_y)
                web_instance.hasPosition_Point_Z.append(web_position_z)

                web_instance.hasPosition_Normal_X.append(web_normal_x)
                web_instance.hasPosition_Normal_Y.append(web_normal_y)
                web_instance.hasPosition_Normal_Z.append(web_normal_z)

                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'web (ID: {web_id}; Position point:({web_position_x},{web_position_y},{web_position_z}); Position normal:({web_normal_x},{web_normal_y},{web_normal_z}))'
                )

        elif line.startswith('corner'):
            match = utils.pattern_corner.match(line)
            if match:
                corner_id = int(match.group(1))
                corner_parent_id = int(match.group(2))
                corner_radius = float(match.group(3))

                # Inserindo na ontologia
                corner_instance = onto.Corner(f'{name}_{corner_id}')
                corner_instance.hasID.append(corner_id)
                corner_instance.hasParentID.append(corner_parent_id)
                corner_instance.hasRadius.append(corner_radius)
                corner_instance.hasName.append(name)


                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'corner (ID: {corner_id}; Parent ID: {corner_parent_id}; Radius: {corner_radius}mm)')

        elif line.startswith('joggle'):
            match = utils.pattern_joggle.match(line)
            if match:
                joggle_id = int(match.group(1))
                joggle_parent_id = int(match.group(2))
                joggle_runout = float(match.group(3))
                joggle_runout_direction_x = float(match.group(4))
                joggle_runout_direction_y = float(match.group(5))
                joggle_runout_direction_z = float(match.group(6))
                joggle_depth = float(match.group(7))
                joggle_depth_direction_x = float(match.group(8))
                joggle_depth_direction_y = float(match.group(9))
                joggle_depth_direction_z = float(match.group(10))
                joggle_bend_Radius_1 = float(match.group(11))
                joggle_bend_Radius_2 = float(match.group(12))
                joggle_type = match.group(13)

                # Inserindo na ontologia
                joggle_instance = onto.Joggle(f'{name}_{joggle_id}')
                joggle_instance.hasID.append(joggle_id)
                joggle_instance.hasParentID.append(joggle_parent_id)
                joggle_instance.hasRunout.append(joggle_runout)
                joggle_instance.hasRunout_Direction_X.append(joggle_runout_direction_x)
                joggle_instance.hasRunout_Direction_Y.append(joggle_runout_direction_y)
                joggle_instance.hasRunout_Direction_Z.append(joggle_runout_direction_z)
                joggle_instance.hasDepth.append(joggle_depth)
                joggle_instance.hasDepth_Direction_X.append(joggle_depth_direction_x)
                joggle_instance.hasDepth_Direction_Y.append(joggle_depth_direction_y)
                joggle_instance.hasDepth_Direction_Z.append(joggle_depth_direction_z)
                joggle_instance.hasBend_Radius_1.append(joggle_bend_Radius_1)
                joggle_instance.hasBend_Radius_2.append(joggle_bend_Radius_2)
                joggle_instance.hasType.append(joggle_type)
                joggle_instance.hasName.append(name)

                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'joggle (ID: {joggle_id}; Parent ID: {joggle_parent_id}; Runout: {joggle_runout} mm; Runout Direction:({joggle_runout_direction_x},{joggle_runout_direction_y},{joggle_runout_direction_z}); Depth: {joggle_depth} mm; Depth Direction:({joggle_depth_direction_x},{joggle_depth_direction_y},{joggle_depth_direction_z}); Bend radius 1: {joggle_bend_Radius_1} mm; Bend radius 2: {joggle_bend_Radius_2} mm; Type: {joggle_type})')


        elif line.startswith('attachment hole'):
            match = utils.pattern_attachment_hole.match(line)
            if match:
                attachment_hole_id = int(match.group(1))
                attachment_hole_parent_id = int(match.group(2))
                attachment_hole_diameter = float(match.group(3))

                attachment_hole_position_x = float(match.group(4))
                attachment_hole_position_y = float(match.group(5))
                attachment_hole_position_z = float(match.group(6))

                attachment_hole_normal_x = float(match.group(7))
                attachment_hole_normal_y = float(match.group(8))
                attachment_hole_normal_z = float(match.group(9))

                # Inserindo na ontologia
                attachment_hole_instance = onto.Attachment_Hole(f'{name}_{attachment_hole_id}')
                attachment_hole_instance.hasID.append(attachment_hole_id)
                attachment_hole_instance.hasParentID.append(attachment_hole_parent_id)
                attachment_hole_instance.hasDiameter.append(attachment_hole_diameter)

                attachment_hole_instance.hasPosition_Point_X.append(attachment_hole_position_x)
                attachment_hole_instance.hasPosition_Point_Y.append(attachment_hole_position_y)
                attachment_hole_instance.hasPosition_Point_Z.append(attachment_hole_position_z)

                attachment_hole_instance.hasPosition_Normal_X.append(attachment_hole_normal_x)
                attachment_hole_instance.hasPosition_Normal_Y.append(attachment_hole_normal_y)
                attachment_hole_instance.hasPosition_Normal_Z.append(attachment_hole_normal_z)
                attachment_hole_instance.hasName.append(name)

                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'attachment hole (ID: {attachment_hole_id}; Parent ID: {attachment_hole_parent_id}; Diameter: {attachment_hole_diameter}mm; Position point:({attachment_hole_position_x},{attachment_hole_position_y},{attachment_hole_position_z}); Position normal:({attachment_hole_normal_x},{attachment_hole_normal_y},{attachment_hole_normal_z})')

        elif line.startswith('tooling hole'):
            match = utils.pattern_tooling_hole.match(line)
            if match:
                tooling_hole_id = int(match.group(1))
                tooling_hole_parent_id = int(match.group(2))
                tooling_hole_diameter = float(match.group(3))

                tooling_hole_position_x = float(match.group(4))
                tooling_hole_position_y = float(match.group(5))
                tooling_hole_position_z = float(match.group(6))

                tooling_hole_normal_x = float(match.group(7))
                tooling_hole_normal_y = float(match.group(8))
                tooling_hole_normal_z = float(match.group(9))

                # Inserindo na ontologia
                tooling_hole_instance = onto.Tooling_Hole(f'{name}_{tooling_hole_id}')
                tooling_hole_instance.hasID.append(tooling_hole_id)
                tooling_hole_instance.hasParentID.append(tooling_hole_parent_id)
                tooling_hole_instance.hasDiameter.append(tooling_hole_diameter)

                tooling_hole_instance.hasPosition_Point_X.append(tooling_hole_position_x)
                tooling_hole_instance.hasPosition_Point_Y.append(tooling_hole_position_y)
                tooling_hole_instance.hasPosition_Point_Z.append(tooling_hole_position_z)

                tooling_hole_instance.hasPosition_Normal_X.append(tooling_hole_normal_x)
                tooling_hole_instance.hasPosition_Normal_Y.append(tooling_hole_normal_y)
                tooling_hole_instance.hasPosition_Normal_Z.append(tooling_hole_normal_z)
                tooling_hole_instance.hasName.append(name)


                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'tooling hole (ID: {tooling_hole_id}; Parent ID: {tooling_hole_parent_id}; Diameter: {tooling_hole_diameter}mm; Position point:({tooling_hole_position_x},{tooling_hole_position_y},{tooling_hole_position_z}); Position normal:({tooling_hole_normal_x},{tooling_hole_normal_y},{tooling_hole_normal_z})')

        elif line.startswith('lightening hole'):
            match = utils.pattern_lightening_hole.match(line)
            if match:
                lightening_hole_id = int(match.group(1))
                lightening_hole_parent_id = int(match.group(2))

                lightening_hole_outer_diameter = float(match.group(3))
                lightening_hole_clearance_diameter = float(match.group(4))
                lightening_hole_height = float(match.group(5))
                lightening_hole_angle = float(match.group(6))
                lightening_hole_bend_radius = float(match.group(7))

                lightening_hole_position_x = float(match.group(8))
                lightening_hole_position_y = float(match.group(9))
                lightening_hole_position_z = float(match.group(10))

                lightening_hole_normal_x = float(match.group(11))
                lightening_hole_normal_y = float(match.group(12))
                lightening_hole_normal_z = float(match.group(13))

                # Inserindo na ontologia
                lightening_hole_instance = onto.Lightening_Hole(f'{name}_{lightening_hole_id}')

                lightening_hole_instance.hasID.append(lightening_hole_id)
                lightening_hole_instance.hasParentID.append(lightening_hole_parent_id)

                lightening_hole_instance.hasOuter_Diameter.append(lightening_hole_outer_diameter)
                lightening_hole_instance.hasClearance_Diameter.append(lightening_hole_clearance_diameter)
                lightening_hole_instance.hasHeight.append(lightening_hole_height)
                lightening_hole_instance.hasAngle.append(lightening_hole_angle)
                lightening_hole_instance.hasBend_Radius.append(lightening_hole_bend_radius)

                lightening_hole_instance.hasPosition_Point_X.append(lightening_hole_position_x)
                lightening_hole_instance.hasPosition_Point_Y.append(lightening_hole_position_y)
                lightening_hole_instance.hasPosition_Point_Z.append(lightening_hole_position_z)

                lightening_hole_instance.hasPosition_Normal_X.append(lightening_hole_normal_x)
                lightening_hole_instance.hasPosition_Normal_Y.append(lightening_hole_normal_y)
                lightening_hole_instance.hasPosition_Normal_Z.append(lightening_hole_normal_z)
                lightening_hole_instance.hasName.append(name)

                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'lightening hole (ID: {lightening_hole_id}; Parent ID: {lightening_hole_parent_id}; Outer diameter: {lightening_hole_outer_diameter}mm; Clearance diameter: {lightening_hole_clearance_diameter}mm; Height: {lightening_hole_height} mm; Angle: {lightening_hole_angle} degree; Bend radius: {lightening_hole_bend_radius} mm; Position point:({lightening_hole_position_x},{lightening_hole_position_y},{lightening_hole_position_z}); Position normal:({lightening_hole_normal_x},{lightening_hole_normal_y},{lightening_hole_normal_z})')

        elif line.startswith('deformed flange'):
            match = utils.pattern_deformed_flange.match(line)
            if match:
                deformed_flange_id = int(match.group(1))
                deformed_flange_parent_id = int(match.group(2))
                deformed_flange_deformation_length = float(match.group(3))

                deformed_flange_instance = onto.Deformed_Flange(f'{name}_{deformed_flange_id}')
                deformed_flange_instance.hasID.append(deformed_flange_id)
                deformed_flange_instance.hasParentID.append(deformed_flange_parent_id)
                deformed_flange_instance.hasDeformation_Length.append(deformed_flange_deformation_length)
                deformed_flange_instance.hasName.append(name)

                print(f"deformed flange (ID: {deformed_flange_id}; Parent ID: {deformed_flange_parent_id}; Deformation Length: {deformed_flange_deformation_length} mm)")
            else:
                match = utils.pattern_deformed_flange2.match(line)
                if match:
                    deformed_flange_id = int(match.group(1))
                    deformed_flange_parent_id = int(match.group(2))

                    deformed_flange_instance = onto.Deformed_Flange(f'{name}_{deformed_flange_id}')
                    deformed_flange_instance.hasID.append(deformed_flange_id)
                    deformed_flange_instance.hasParentID.append(deformed_flange_parent_id)
                    deformed_flange_instance.hasName.append(name)
                    try:
                        deformed_flange_instance.hasDeformation_Length.append(deformed_flange_deformation_length)
                    except:
                        deformed_flange_instance.hasDeformation_Length.append(0)


#                    print(f"deformed flange (ID: {deformed_flange_id}; Parent ID: {deformed_flange_parent_id}; Deformation Length obtained: {deformed_flange_deformation_length} mm)")

        elif line.startswith('stiffening flange'):
            match = utils.pattern_stiffening_flange.match(line)
            if match:
                stiffening_flange_id = int(match.group(1))
                stiffening_flange_parent_id = int(match.group(2))
                stiffening_flange_width = float(match.group(3))
                stiffening_flange_length = float(match.group(4))
                stiffening_flange_bend_radius = float(match.group(5))
                stiffening_flange_type = match.group(6)

                stiffening_flange_position_x = float(match.group(7))
                stiffening_flange_position_y = float(match.group(8))
                stiffening_flange_position_z = float(match.group(9))

                stiffening_flange_normal_x = float(match.group(10))
                stiffening_flange_normal_y = float(match.group(11))
                stiffening_flange_normal_z = float(match.group(12))

                # Inserindo na ontologia
                stiffening_flange_instance = onto.Stiffening_Flange(f'{name}_{stiffening_flange_id}')
                stiffening_flange_instance.hasID.append(stiffening_flange_id)
                stiffening_flange_instance.hasParentID.append(stiffening_flange_parent_id)
                stiffening_flange_instance.hasWidth.append(stiffening_flange_width)
                stiffening_flange_instance.hasLength.append(stiffening_flange_length)
                stiffening_flange_instance.hasBend_Radius.append(stiffening_flange_bend_radius)
                stiffening_flange_instance.hasType.append(stiffening_flange_type)

                stiffening_flange_instance.hasPosition_Point_X.append(stiffening_flange_position_x)
                stiffening_flange_instance.hasPosition_Point_Y.append(stiffening_flange_position_y)
                stiffening_flange_instance.hasPosition_Point_Z.append(stiffening_flange_position_z)

                stiffening_flange_instance.hasPosition_Normal_X.append(stiffening_flange_normal_x)
                stiffening_flange_instance.hasPosition_Normal_Y.append(stiffening_flange_normal_y)
                stiffening_flange_instance.hasPosition_Normal_Z.append(stiffening_flange_normal_z)
                stiffening_flange_instance.hasName.append(name)

                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'stiffening flange (ID: {stiffening_flange_id}; Parent ID: {stiffening_flange_parent_id}; Width: {stiffening_flange_width}mm; Length: {stiffening_flange_length}mm; Bend Radius: {stiffening_flange_bend_radius} mm; Type: {stiffening_flange_type}; Position point:({stiffening_flange_position_x},{stiffening_flange_position_y},{stiffening_flange_position_z}); Position normal:({stiffening_flange_normal_x},{stiffening_flange_normal_y},{stiffening_flange_normal_z})')


        elif line.startswith('attachment flange'):
            match = utils.pattern_attachment_flange.match(line)
            if match:
                attachment_flange_id = int(match.group(1))
                attachment_flange_parent_id = int(match.group(2))
                attachment_flange_width = float(match.group(3))
                attachment_flange_length = float(match.group(4))
                attachment_flange_bend_radius = float(match.group(5))
                attachment_flange_type = match.group(6)

                attachment_flange_position_x = float(match.group(7))
                attachment_flange_position_y = float(match.group(8))
                attachment_flange_position_z = float(match.group(9))

                attachment_flange_normal_x = float(match.group(10))
                attachment_flange_normal_y = float(match.group(11))
                attachment_flange_normal_z = float(match.group(12))

                # Inserindo na ontologia
                attachment_flange_instance = onto.Attachment_Flange(f'{name}_{attachment_flange_id}')
                attachment_flange_instance.hasID.append(attachment_flange_id)
                attachment_flange_instance.hasParentID.append(attachment_flange_parent_id)
                attachment_flange_instance.hasWidth.append(attachment_flange_width)
                attachment_flange_instance.hasLength.append(attachment_flange_length)
                attachment_flange_instance.hasBend_Radius.append(attachment_flange_bend_radius)

                attachment_flange_instance.hasPosition_Point_X.append(attachment_flange_position_x)
                attachment_flange_instance.hasPosition_Point_Y.append(attachment_flange_position_y)
                attachment_flange_instance.hasPosition_Point_Z.append(attachment_flange_position_z)

                attachment_flange_instance.hasPosition_Normal_X.append(attachment_flange_normal_x)
                attachment_flange_instance.hasPosition_Normal_Y.append(attachment_flange_normal_y)
                attachment_flange_instance.hasPosition_Normal_Z.append(attachment_flange_normal_z)
                attachment_flange_instance.hasName.append(name)


                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'attachment flange (ID: {attachment_flange_id}; Parent ID: {attachment_flange_parent_id}; Width: {attachment_flange_width}mm; Length: {attachment_flange_length}mm; Bend Radius: {attachment_flange_bend_radius} mm; Type: {attachment_flange_type}; Position point:({attachment_flange_position_x},{attachment_flange_position_y},{attachment_flange_position_z}); Position normal:({attachment_flange_normal_x},{attachment_flange_normal_y},{attachment_flange_normal_z})')

        elif line.startswith('stringer cutout'):
            match = utils.pattern_stringer_cutout.match(line)
            if match:
                stringer_cutout_id = int(match.group(1))
                stringer_cutout_parent_id = int(match.group(2))
                stringer_cutout_profile = [(float(match.group(i)), float(match.group(i + 1)), float(match.group(i + 2)))
                                           for i in range(3, 20, 3)]

                # Inserindo na ontologia
                stringer_cutout_instance = onto.Stringer_Cutout(f'{name}_{stringer_cutout_id}')
                stringer_cutout_instance.hasID.append(stringer_cutout_id)
                stringer_cutout_instance.hasParentID.append(stringer_cutout_parent_id)
                stringer_cutout_instance.hasProfile.extend(stringer_cutout_profile)
                stringer_cutout_instance.hasName.append(name)

                print(
                    f'VALORES INSERIDOS NA ONTOLOGIA: '
                    f'stringer cutout (ID: {stringer_cutout_id}; Parent ID: {stringer_cutout_parent_id}; Profile: {stringer_cutout_profile})')


        elif line.startswith('bead'):
            match = utils.pattern_bead.match(line)
            if match:
                bead_id = int(match.group(1))
                bead_parent_id = int(match.group(2))
                bead_width = float(match.group(3))
                bead_depth = float(match.group(4))
                # Inserindo na ontologia
                bead_instance = onto.Bead(f'{name}_{bead_id}')
                bead_instance.hasID.append(bead_id)
                bead_instance.hasParentID.append(bead_parent_id)
                bead_instance.hasWidth.append(bead_width)
                bead_instance.hasDepth.append(bead_depth)
                bead_instance.hasName.append(name)

        elif line.startswith('cutout'):
            match = utils.pattern_cutout.match(line)
            if match:
                cutout_id = int(match.group(1))
                cutout_parent_id = int(match.group(2))
                cutout_profile = [float(match.group(i)) for i in range(3, 15)]
                # Inserindo na ontologia
                cutout_instance = onto.Cutout(f'{name}_{cutout_id}')
                cutout_instance.hasID.append(cutout_id)
                cutout_instance.hasParentID.append(cutout_parent_id)
                cutout_instance.hasProfile.append(cutout_profile)
                cutout_instance.hasName.append(name)

        elif line.startswith('lip'):
            match = utils.pattern_lip.match(line)
            if match:
                lip_id = int(match.group(1))
                lip_parent_id = int(match.group(2))
                lip_width = float(match.group(3))
                lip_length = float(match.group(4))
                # Inserindo na ontologia
                lip_instance = onto.Lip(f'{name}_{lip_id}')
                lip_instance.hasID.append(lip_id)
                lip_instance.hasParentID.append(lip_parent_id)
                lip_instance.hasWidth.append(lip_width)
                lip_instance.hasLength.append(lip_length)
                lip_instance.hasName.append(name)

        elif line.startswith('twin joggle'):
            match = utils.pattern_twin_joggle.match(line)
            if match:
                twin_joggle_id = int(match.group(1))
                twin_joggle_parent_id = int(match.group(2))
                twin_joggle_runout = float(match.group(3))
                twin_joggle_runout_dir = [float(match.group(i)) for i in range(4, 7)]
                twin_joggle_depth = float(match.group(7))
                twin_joggle_depth_dir = [float(match.group(i)) for i in range(8, 11)]
                twin_joggle_type = match.group(11)

                # Inserindo na ontologia
                twin_joggle_instance = onto.Twin_Joggle(f'{name}_{twin_joggle_id}')
                twin_joggle_instance.hasID.append(twin_joggle_id)
                twin_joggle_instance.hasParentID.append(twin_joggle_parent_id)
                twin_joggle_instance.hasRunout.append(twin_joggle_runout)
                twin_joggle_instance.hasRunout_Direction_X.append(twin_joggle_runout_dir[0])
                twin_joggle_instance.hasRunout_Direction_Y.append(twin_joggle_runout_dir[1])
                twin_joggle_instance.hasRunout_Direction_Z.append(twin_joggle_runout_dir[2])
                twin_joggle_instance.hasDepth.append(twin_joggle_depth)
                twin_joggle_instance.hasDepth_Direction_X.append(twin_joggle_depth_dir[0])
                twin_joggle_instance.hasDepth_Direction_Y.append(twin_joggle_depth_dir[1])
                twin_joggle_instance.hasDepth_Direction_Z.append(twin_joggle_depth_dir[2])
                twin_joggle_instance.hasType.append(twin_joggle_type)
                twin_joggle_instance.hasName.append(name)

        elif line.startswith('bend relief'):
            match = utils.pattern_bend_relief.match(line)
            if match:
                bend_relief_id = int(match.group(1))
                parent_id1 = int(match.group(2))
                parent_id2 = int(match.group(3))
                bend_relief_radius = float(match.group(4))

                # Inserindo na ontologia
                bend_relief_instance = onto.Bend_Relief(f'{name}_{bend_relief_id}')
                bend_relief_instance.hasID.append(bend_relief_id)
                bend_relief_instance.hasParentID.append(parent_id1)
                bend_relief_instance.hasParentID.append(parent_id2)
                bend_relief_instance.hasRadius.append(bend_relief_radius)
                bend_relief_instance.hasName.append(name)

                print(f'bend relief (ID: {bend_relief_id}; Parents IDs: {parent_id1}, {parent_id2}; Radius: {bend_relief_radius} mm)')

def insert_data_new(onto, file_path):
    """
    Coleta os dados de uma peça e insere em uma ontologia com base nos padrões encontrados em um arquivo.

    Args:
        onto: Ontologia onde os dados serão inseridos.
        file_path (str): Caminho completo do arquivo contendo os dados a serem inseridos.
    """


    with open(file_path, 'r') as file:
        lines = file.readlines()

    last_deformation_length = None

    for line in lines:
        if re.match(utils.pattern_web, line):
            match = re.match(utils.pattern_web, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasPosition_Point_X': float(data[1]),
                'hasPosition_Point_Y': float(data[2]),
                'hasPosition_Point_Z': float(data[3]),
                'hasPosition_Normal_X': float(data[4]),
                'hasPosition_Normal_Y': float(data[5]),
                'hasPosition_Normal_Z': float(data[6])
            }
            print(data_dict)
            insert_instance(onto, "Web", **data_dict)

        elif re.match(utils.pattern_corner, line):
            match = re.match(utils.pattern_corner, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasRadius': float(data[2])
            }
            insert_instance(onto, 'Corner', **data_dict)

        elif re.match(utils.pattern_lightening_hole, line):
            match = re.match(utils.pattern_lightening_hole, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasOuter_Diameter': float(data[2]),
                'hasClearance_Diameter': float(data[3]),
                'hasHeight': float(data[4]),
                'hasAngle': float(data[5]),
                'hasBend_Radius': float(data[6]),
                'hasPosition_Point_X': float(data[7]),
                'hasPosition_Point_Y': float(data[8]),
                'hasPosition_Point_Z': float(data[9]),
                'hasPosition_Normal_X': float(data[10]),
                'hasPosition_Normal_Y': float(data[11]),
                'hasPosition_Normal_Z': float(data[12])
            }
            insert_instance(onto, 'Lightening_Hole', **data_dict)

        elif re.match(utils.pattern_tooling_hole, line):
            match = re.match(utils.pattern_tooling_hole, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasDiameter': float(data[2]),
                'hasPosition_Point_X': float(data[3]),
                'hasPosition_Point_Y': float(data[4]),
                'hasPosition_Point_Z': float(data[5]),
                'hasPosition_Normal_X': float(data[6]),
                'hasPosition_Normal_Y': float(data[7]),
                'hasPosition_Normal_Z': float(data[8])
            }
            insert_instance(onto, "Tooling_Hole", **data_dict)

        elif re.match(utils.pattern_attachment_hole, line):
            match = re.match(utils.pattern_attachment_hole, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasDiameter': float(data[2]),
                'hasPosition_Point_X': float(data[3]),
                'hasPosition_Point_Y': float(data[4]),
                'hasPosition_Point_Z': float(data[5]),
                'hasPosition_Normal_X': float(data[6]),
                'hasPosition_Normal_Y': float(data[7]),
                'hasPosition_Normal_Z': float(data[8])
            }
            insert_instance(onto, 'Attachment_Hole', **data_dict)

        elif re.match(utils.pattern_attachment_flange, line):
            match = re.match(utils.pattern_attachment_flange, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasLength': float(data[3]),
                'hasBend_Radius': float(data[4]),
                'hasType': str(data[5]),
                'hasPosition_Point_X': float(data[6]),
                'hasPosition_Point_Y': float(data[7]),
                'hasPosition_Point_Z': float(data[8]),
                'hasPosition_Normal_X': float(data[9]),
                'hasPosition_Normal_Y': float(data[10]),
                'hasPosition_Normal_Z': float(data[11])
            }
            insert_instance(onto, "Attachment_Flange", **data_dict)

        elif re.match(utils.pattern_stiffening_flange, line):
            match = re.match(utils.pattern_stiffening_flange, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasLength': float(data[3]),
                'hasBend_Radius': float(data[4]),
                'hasType': str(data[5]),
                'hasPosition_Point_X': float(data[6]),
                'hasPosition_Point_Y': float(data[7]),
                'hasPosition_Point_Z': float(data[8]),
                'hasPosition_Normal_X': float(data[9]),
                'hasPosition_Normal_Y': float(data[10]),
                'hasPosition_Normal_Z': float(data[11])
            }
            insert_instance(onto, 'Stiffening_Flange', **data_dict)

        elif re.match(utils.pattern_deformed_flange, line):
            match = re.match(utils.pattern_deformed_flange, line)
            if match:
                data = match.groups()
                last_deformation_length = float(data[2])
                data_dict = {
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasDeformation_length': float(data[2])
                }
            else:
                match = re.match(utils.pattern_deformed_flange2, line)
                data = match.groups()
                data_dict = {
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasDeformation_length': last_deformation_length
                }
            insert_instance(onto, 'Deformed_Flange', **data_dict)

        elif re.match(utils.pattern_joggle, line):
            match = re.match(utils.pattern_joggle, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasRunout': float(data[2]),
                'hasRunout_Direction_X': float(data[3]),
                'hasRunout_Direction_Y': float(data[4]),
                'hasRunout_Direction_Z': float(data[5]),
                'hasDepth': float(data[6]),
                'hasDepth_Direction_X': float(data[7]),
                'hasDepth_Direction_Y': float(data[8]),
                'hasDepth_Direction_Z': float(data[9]),
                'hasBend_Radius_1': float(data[10]),
                'hasBend_Radius_2': float(data[11]),
                'hasType': str(data[12])
            }
            insert_instance(onto, 'Joggle', **data_dict)

        elif re.match(utils.pattern_twin_joggle, line):
            match = re.match(utils.pattern_twin_joggle, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasRunout': float(data[2]),
                'hasRunout_Direction_X': float(data[3]),
                'hasRunout_Direction_Y': float(data[4]),
                'hasRunout_Direction_Z': float(data[5]),
                'hasDepth': float(data[6]),
                'hasDepth_Direction_X': float(data[7]),
                'hasDepth_Direction_Y': float(data[8]),
                'hasDepth_Direction_Z': float(data[9]),
                'hasBend_Radius_1': float(data[10]),
                'hasBend_Radius_2': float(data[11]),
                'hasType': str(data[12])
            }
            insert_instance(onto, 'Twin_Joggle', **data_dict)

        elif re.match(utils.pattern_bend_relief, line):
            match = re.match(utils.pattern_bend_relief, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]).split(','),  # Convert comma-separated parents to a list
                'hasRadius': float(data[2])
            }
            insert_instance(onto, "Bend_Relief", **data_dict)

        elif re.match(utils.pattern_stringer_cutout, line):
            match = re.match(utils.pattern_stringer_cutout, line)
            data = match.groups()
            points = []
            for i in range(0, 18, 3):
                points.append((float(data[i]), float(data[i + 1]), float(data[i + 2])))
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasProfile': points
            }
            insert_instance(onto, "Stringer_Cutout", **data_dict)

        elif re.match(utils.pattern_cutout, line):
            match = re.match(utils.pattern_cutout, line)
            data = match.groups()
            points = []
            for i in range(0, 18, 3):
                points.append((float(data[i]), float(data[i + 1]), float(data[i + 2])))
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasProfile': points
            }
            insert_instance(onto, "Cutout", **data_dict)

        elif re.match(utils.pattern_bead, line):
            match = re.match(utils.pattern_bead, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasDepth': float(data[3])
            }
            insert_instance(onto, "Bead", **data_dict)

        elif re.match(utils.pattern_lip, line):
            match = re.match(utils.pattern_lip, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasLength': float(data[3])
            }
            insert_instance(onto, 'Lip', **data_dict)


# INSERE UMA INSTÂNCIA NA ONTOLOGIA COM OS DADOS DA PEÇA
def insert_instance(onto, class_name, **kwargs):
    """
    Insere instâncias de uma classe específica na ontologia.

    Args:
        onto: Ontologia onde as instâncias serão inseridas.
        class_name (str): Nome da classe na qual as instâncias serão inseridas.
        **kwargs: Argumentos nomeados representando propriedades e seus valores para as instâncias AFR_Output serem inseridas.
    """

    # Obtém AFR_Output classe correspondente na ontologia
    target_class = getattr(onto, class_name, None)

    if target_class is None:
        print(f"Classe '{class_name}' não encontrada na ontologia.")
        return

    # Cria uma nova instância da classe alvo
    new_instance = target_class()

    # Itera sobre os argumentos nomeados e define as propriedades das instâncias
    for prop_name, value in kwargs.items():

        if hasattr(new_instance, prop_name):
            prop = getattr(new_instance, prop_name)
            if isinstance(prop, list):
                # Se for uma lista, adicione o valor à lista
                prop.append(value)
            else:
                # Se não for uma lista, defina o valor diretamente
                setattr(new_instance, prop_name, value)
            # prop = getattr(new_instance, prop_name)
            # prop.append(value)
        else:
            print(f"Propriedade '{prop_name}' não encontrada na classe '{class_name}'.")

    print(f"Instância inserida na ontologia: {new_instance}")
