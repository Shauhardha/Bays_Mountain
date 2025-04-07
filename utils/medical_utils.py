from database.postgresql_connection import init_postgres_connection

def add_injury_log(user_id, datetime, animal_group, individual_name, encounter_type, injury_type, injury_desc, exam_type):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO injury_log (user_id, datetime, animal_group, individual_name, encounter_type, injury_type, injury_desc, exam_type)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, injury_type, injury_desc, exam_type)
    cursor.execute(query, params)
    injury_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return injury_id

def add_sedation_log(user_id, datetime, animal_group, individual_name, encounter_type, sedation_med, dose, sedation_kit, sedation_route, time_in, time_out):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO sedation_log (user_id, datetime, animal_group, individual_name, encounter_type, sedation_med, dose, sedation_kit, sedation_route, time_in, time_out)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, sedation_med, dose, sedation_kit, sedation_route, time_in, time_out)
    cursor.execute(query, params)
    sedation_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return sedation_id

def add_medslog(user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken,Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,Meloxicam_dose,Cephalexin_dose,Gabapentin_dose,Bravecto_dose,Intercepter_dose,IfOther):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO med_log (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken,
    Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,Meloxicam_dose,Cephalexin_dose,Gabapentin_dose,Bravecto_dose,Intercepter_dose,IfOther)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken, Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,Meloxicam_dose,Cephalexin_dose,Gabapentin_dose,Bravecto_dose,Intercepter_dose,IfOther)
    cursor.execute(query, params)
    med_log_id = cursor.fetchone()[0] 
    conn.commit()
    conn.close()
    return med_log_id

def add_medslog_main(user_id, datetime, animal_group, individual_name, encounter_type, tied_to_injury, injury_id, animal_sedated, sedation_id, vet_notified, vet_response, meds_given, med_id, med_notes):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO med_log_main (user_id, datetime, animal_group, individual_name, encounter_type, tied_to_injury, injury_id, animal_sedated, sedation_id, vet_notified, vet_response, meds_given, med_id, med_notes)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, tied_to_injury, injury_id, animal_sedated, sedation_id, vet_notified, vet_response, meds_given, med_id, med_notes)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_vetlog(user_id, datetime, animal_group, individual_name, vet_name, check_type, vet_location, vet_notes):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO vet_log (user_id, datetime, animal_group, individual_name, vet_name, check_type, vet_location, vet_notes)
    VALUES (%s, %s, %s, INITCAP(%s), INITCAP(%s), %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, individual_name, vet_name, check_type, vet_location, vet_notes)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_watershed_med_log(user_id, datetime, individual, observation, intervention, notes):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO watershed_med_log (user_id, datetime, individual, observation, intervention, watershed_med_notes)
    VALUES (%s, %s, INITCAP(%s), %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, individual, observation, intervention, notes)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_herp_med_log(user_id, datetime, individual, observation, intervention, notes):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO herp_med_log (user_id, datetime, individual, observation, intervention, herp_med_notes)
    VALUES (%s, %s, INITCAP(%s), %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, individual, observation, intervention, notes)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
