class Globals:
    global_time_frame = 0.0
    pheromone_drop_rate = 3
    update_pheromones_count = 1
    pheromone_lifespan = 7
    ant_FOV = 5
    pheromone_drop_FOV = 3
    exploration_rate = 0.005
    col1_ants_generated = 250
    col2_ants_generated = 0
    delay_rate = 0
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
    pheromones_to_check = 10
    how_young_pheromone_to_consider = 10
    chance_to_deviate_from_path = 0
    colonies = []
    food_sources = []
    pheromones = []
    width = 1520
    height = 900
    matrix = []
    how_many_pheromone_drops_to_check = 10
    how_long_until_ant_forgets_last_pheromone = 5
    time_until_pheromone_override = 1
    avg_pheromone_creation_time = 0
    new_count = 1

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01

    @staticmethod
    def initialize_matrix():
        Globals.matrix = [[None for _ in range(Globals.width)] for _ in range(Globals.height)]
