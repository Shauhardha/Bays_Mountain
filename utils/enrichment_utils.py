from database.postgresql_connection import init_postgres_connection

def add_enrichment_log(user_id, datetime, animal_group, enrichment_response, individual_name, enrichment_type, enrichment_details, time_in, time_out, observation_type, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO enrichment_log (user_id, datetime, animal_group, enrichment_response, individual_name, enrichment_type, enrichment_details, time_in, time_out, observation_type, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, enrichment_response, individual_name, enrichment_type, enrichment_details, time_in, time_out, observation_type, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_watershed_care_log(user_id, datetime, location, care_performed, other_care, watershed_care_notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO watershed_care_log (user_id, datetime, location, care_performed, other_care, watershed_care_notes, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, location, care_performed, other_care, watershed_care_notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
def add_herp_care_log(user_id, datetime, animal_type, care_performed, other_care, enclosures_not_done, herp_care_notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO herp_care_log (user_id, datetime, animal_type, care_performed, other_care, enclosures_not_done, herp_care_notes, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_type, care_performed, other_care, enclosures_not_done, herp_care_notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
