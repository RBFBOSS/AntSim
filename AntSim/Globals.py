class Globals:
    global_time_frame = 0.0
    pheromone_drop_rate = 3
    update_pheromones_count = 1
    pheromone_lifespan = 7
    ants_FOV = 8
    exploration_rate = 0.005
    col1_ants_generated = 100
    col2_ants_generated = 0
    delay_rate = 0.01
    avg_object_sighted_time = 0
    avg_pheromone_drop_time = 0
    avg_move_time = 0
    avg_perform_action_time = 0
    avg_placement_time = 0
    ant_operations = 0
    objects_sighted = 0
    entire_time = 0
    pheromones_sighted = 0
    colonies_sighted = 0
    ants_sighted = 0
    food_sources_sighted = 0
    speed = 1
    how_recent_last_visit_has_to_be_for_pheromone_drop = 20
    pheromones_to_check = 50
    how_old_pheromone_to_consider = 0.5
    chance_to_deviate_from_path = 0.05

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01
