from database.postgresql_connection import init_postgres_connection
import pandas as pd

def add_injury_log(user_id, datetime, animal_group, individual_name, encounter_type, injury_type, injury_desc, exam_type, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO injury_log (user_id, datetime, animal_group, individual_name, encounter_type, injury_type, injury_desc, exam_type, log_time)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, injury_type, injury_desc, exam_type, log_time)
    cursor.execute(query, params)
    injury_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return injury_id

def add_sedation_log(user_id, datetime, animal_group, individual_name, encounter_type, sedation_med, dose, sedation_kit, sedation_route, time_in, time_out, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO sedation_log (user_id, datetime, animal_group, individual_name, encounter_type, sedation_med, dose, sedation_kit, sedation_route, time_in, time_out, log_time)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, sedation_med, dose, sedation_kit, sedation_route, time_in, time_out, log_time)
    cursor.execute(query, params)
    sedation_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return sedation_id

def add_medslog(user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken,Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,Meloxicam_dose,Cephalexin_dose,Gabapentin_dose,Bravecto_dose,Intercepter_dose,IfOther, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO med_log (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken,
    Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,Meloxicam_dose,Cephalexin_dose,Gabapentin_dose,Bravecto_dose,Intercepter_dose,IfOther, log_time)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken, Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,Meloxicam_dose,Cephalexin_dose,Gabapentin_dose,Bravecto_dose,Intercepter_dose,IfOther, log_time)
    cursor.execute(query, params)
    med_log_id = cursor.fetchone()[0] 
    conn.commit()
    conn.close()
    return med_log_id

def add_medslog_main(user_id, datetime, animal_group, individual_name, encounter_type, tied_to_injury, injury_id, animal_sedated, sedation_id, vet_notified, vet_response, meds_given, med_id, med_notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO med_log_main (user_id, datetime, animal_group, individual_name, encounter_type, tied_to_injury, injury_id, animal_sedated, sedation_id, vet_notified, vet_response, meds_given, med_id, med_notes, log_time)
    VALUES (%s, %s, %s, INITCAP(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, tied_to_injury, injury_id, animal_sedated, sedation_id, vet_notified, vet_response, meds_given, med_id, med_notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_vetlog(user_id, datetime, animal_group, individual_name, vet_name, check_type, vet_location, vet_notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO vet_log (user_id, datetime, animal_group, individual_name, vet_name, check_type, vet_location, vet_notes, log_time)
    VALUES (%s, %s, %s, INITCAP(%s), INITCAP(%s), %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, individual_name, vet_name, check_type, vet_location, vet_notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_watershed_med_log(user_id, datetime, individual, observation, intervention, notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO watershed_med_log (user_id, datetime, individual, observation, intervention, watershed_med_notes, log_time)
    VALUES (%s, %s, INITCAP(%s), %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, individual, observation, intervention, notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_herp_med_log(user_id, datetime, individual, observation, intervention, notes, log_time):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO herp_med_log (user_id, datetime, individual, observation, intervention, herp_med_notes, log_time)
    VALUES (%s, %s, INITCAP(%s), %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, individual, observation, intervention, notes, log_time)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_meds_data(from_date, to_date):
    conn = init_postgres_connection()
    cursor = conn.cursor()

    query_string = """
        select 
            (select initcap(username) from users u where a.user_id = u.user_id) as UserName,
            datetime,
            animal_group as "Animal",
            administration_route,
			meds_taken,
			meloxicam as "Meloxicam",
			cephalexin as "Cephalexin",
			gabapentin as "Gabapentin",
			bravecto as "Bravecto",
			intercepter as "Intercepter"
			from med_log a
			where datetime between %s and %s
    """
    # params = [f'%{from_date}%', f'%{to_date}%']
    # cursor.execute(query_string, params)
    # reminders = cursor.fetchall()
    df = pd.read_sql_query(query_string, conn, params=(from_date, to_date))
    conn.close()
    return df