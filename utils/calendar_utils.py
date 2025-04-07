from database.postgresql_connection import init_postgres_connection

def add_reminder(user_id, date, title, description, assigned_to=None, priority="Medium"):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO reminders (user_id, date, title, description, assigned_to, priority)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (user_id, date, title, description, assigned_to, priority)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def update_reminder(reminder_id, date, title, description, assigned_to, priority):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE reminders
            SET date = %s, title = %s, description = %s, assigned_to = %s, priority = %s
            WHERE id = %s
        """, (date, title, description, assigned_to, priority, reminder_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating reminder: {e}")
        return False
    finally:
        conn.close()

def get_users():
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, username, email FROM users order by user_id"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return users

def get_users_det(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, username, email FROM users WHERE user_id = %s"
    params = (user_id)
    cursor.execute(query, params)
    user = cursor.fetchone() 
    conn.close()
    if user:
        return f"{user[1]} ({user[2]})"  # user[1] = username, user[2] = email
    else:
        return "User not found"

def get_reminders(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    SELECT id, date, title, description, assigned_to, priority
    FROM reminders
    WHERE user_id = %s
    """
    params = ([user_id])
    cursor.execute(query, params)
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def get_all_reminders(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query_string = """
    SELECT id, date, title, description, 
    (SELECT username FROM Users u WHERE u.user_id = r.assigned_to) AS assigned_to, 
    priority
    FROM reminders r
    """
    if user_id:
        query_string += " where assigned_to = %s order by date"
        cursor.execute(query_string, [user_id])
    else:
        query_string += "order by date desc"
        cursor.execute(query_string)
    
    reminders_all = cursor.fetchall()
    conn.close()
    return reminders_all

def delete_reminder(reminder_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = %s", (reminder_id,))
    conn.commit()
    conn.close()

def search_reminders(query, user_id, priority=None, assigned_to=None):
    conn = init_postgres_connection()
    cursor = conn.cursor()

    query_string = """
        SELECT 
            id, 
            date, 
            title, 
            description, 
            assigned_to,
            priority, 
            created_at
        FROM reminders r
        WHERE user_id = %s and
            (title ILIKE %s OR description ILIKE %s)
    """
    params = [user_id, f'%{query}%', f'%{query}%']

    if priority:
        query_string += " AND priority = %s"
        params.append(priority)
    if assigned_to:
        query_string += " AND assigned_to = %s"
        params.append(assigned_to)

    cursor.execute(query_string, params)
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def get_assigned_reminders(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    SELECT id, date, title, description, assigned_to, priority, user_id
    FROM reminders
    WHERE assigned_to = %s
    """
    params = ([user_id])
    cursor.execute(query, params)
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def search_assigned_reminders(query, user_id, priority=None, assigned_to=None):
    conn = init_postgres_connection()
    cursor = conn.cursor()

    query_string = """
        SELECT 
            id, 
            date, 
            title, 
            description, 
            (SELECT username FROM Users u WHERE u.user_id = r.assigned_to) AS assigned_to,
            priority,
            user_id
        FROM reminders r
        WHERE assigned_to = %s and
            (title ILIKE %s OR description ILIKE %s)
    """
    params = [user_id, f'%{query}%', f'%{query}%']

    if priority:
        query_string += " AND priority = %s"
        params.append(priority)
    if assigned_to:
        query_string += " AND assigned_to = %s"
        params.append(assigned_to)

    cursor.execute(query_string, params)
    reminders = cursor.fetchall()
    conn.close()
    return reminders