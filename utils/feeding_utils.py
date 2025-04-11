from database.postgresql_connection import init_postgres_connection
import pandas as pd

def add_feedinglog(user_id, datetime, animal_group, individual_name, food_type, amount_fed, observation_type, leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
                   nb_amount_fed, chicken_amount_fed, prey_amount_fed, fruits_amount_fed, veg_amount_fed, fish_amount_fed, mazuri_amount_fed, total_food_quantity, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO feeding_logs (user_id, datetime, animal_group, individual_name, food_type, amount_fed, observation_type, 
    leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
    Nebraska, Chicken, WholePrey, Fruits, Vegetables, Fish, Mazuri, total_food_quantity, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, individual_name, food_type, amount_fed, observation_type, leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
              nb_amount_fed, chicken_amount_fed, prey_amount_fed, fruits_amount_fed, veg_amount_fed, fish_amount_fed, mazuri_amount_fed, total_food_quantity, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_medslog(user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO med_log (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken, log_time)
    cursor.execute(query, params)
    med_log_id = cursor.fetchone()[0] 
    conn.commit()
    conn.close()
    return med_log_id

def add_watershed_feeding_log(user_id, datetime, location, food_item, other_food, food_amount, indv_not_eating_food, notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO watershed_feeding_log (user_id, datetime, location, food_item, other_food, food_amount, indv_not_eating_food, watershed_feeding_notes, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, location, food_item, other_food, food_amount, indv_not_eating_food, notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
def add_herp_feeding_log(user_id, datetime, animal_type, food_item, other_food, food_amount, indv_not_eating_food, notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO herp_feeding_log (user_id, datetime, animal_type, food_item, other_food, food_amount, indv_not_eating_food, herp_feeding_notes, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_type, food_item, other_food, food_amount, indv_not_eating_food, notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_mammal_data(from_date, to_date):
    conn = init_postgres_connection()
    cursor = conn.cursor()

    query_string = """
        select 
            (select initcap(username) from users u where a.user_id = u.user_id) as UserName,
            datetime,
            animal_group,
            individual_name,
            food_type as other_food,
            amount_fed::float as "OTHER",
            observation_type,
            leftover_food,
            deer_feed_scoops,
            individual_notes,
            nebraska::float as "Nebraska Brand",
            chicken::float as "Chicken",
            wholeprey::float as "Whole Prey",
            fruits::float as "Fresh Fruits",
            vegetables::float as "Fresh Vegetables",
            fish::float as "Fish",
            mazuri::float as "Mazuri Omnivore"
        from feeding_logs a
        where datetime between %s and %s
    """
    # params = [f'%{from_date}%', f'%{to_date}%']
    # cursor.execute(query_string, params)
    # reminders = cursor.fetchall()
    df = pd.read_sql_query(query_string, conn, params=(from_date, to_date))
    conn.close()
    return df