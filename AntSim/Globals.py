import threading


class Globals:
    bloodbath_range = 25
    bloodbath_percentage = 0.25
    attack_cooldown = 50
    attack_range = 1
    time_until_worker_signals_enemies_again = 0
    time_until_colony_stops_making_soldiers = 2000
    max_workers_per_colony = 75
    max_soldiers_per_colony = 25
    worker_production_cost = 2
    soldier_production_cost = 5
    worker_maintenance_cost = 1
    soldier_maintenance_cost = 2
    precise_search_time = 0
    precise_searches = 0
    ants_eat_every_x_turns = 800
    food_source_counter = 0
    nr_of_food_sources = 3
    ant_FOVs = []
    speed = 2
    pause_event = threading.Event()
    waiting_event = threading.Event()
    global_time_frame = 0.0
    pheromone_drop_rate = 2
    update_pheromones_count = 1
    pheromone_lifespan = 6
    ant_FOV = 10
    pheromone_drop_FOV = 5
    exploration_rate = 0.005
    col1_ants_generated = 10
    col2_ants_generated = 10
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
    how_recent_last_visit_has_to_be_for_pheromone_drop = 7
    pheromones_to_check = 10
    how_young_pheromone_to_consider = 10
    chance_to_deviate_from_path = 0
    colonies = []
    food_sources = []
    pheromones = []
    width = 1300
    height = 700
    matrix = []
    how_many_pheromone_drops_to_check = 10
    how_long_until_ant_forgets_last_pheromone = 5
    time_until_pheromone_override = 1
    avg_pheromone_creation_time = 0
    new_count = 1

    @staticmethod
    def pause_pheromone_cleanup():
        Globals.pause_event.set()

    @staticmethod
    def resume_pheromone_cleanup():
        Globals.pause_event.clear()

    @staticmethod
    def is_cleanup_thread_waiting():
        return Globals.waiting_event.is_set()

    @staticmethod
    def increment_time_frame():
        Globals.global_time_frame += 0.01

    @staticmethod
    def initialize_matrix():
        Globals.matrix = [[None for _ in range(Globals.width)] for _ in range(Globals.height)]

    @staticmethod
    def remove_from_food_source(creator, amount):
        for food_source in Globals.food_sources:
            if food_source.food_id == creator:
                food_source.remove_food(amount)
                return

    @staticmethod
    def add_food_to_colony(colony_id, amount):
        for colony in Globals.colonies:
            if colony.colony_id == colony_id:
                colony.add_food(amount)
                return

    @staticmethod
    def colony_received_warning(colony_id):
        for colony in Globals.colonies:
            if colony.colony_id == colony_id:
                colony.start_making_soldiers()
                return

    @staticmethod
    def destroy_ant(colony_id, ant):
        for colony in Globals.colonies:
            if colony.colony_id == colony_id:
                colony.delete_ant(ant)
                return
