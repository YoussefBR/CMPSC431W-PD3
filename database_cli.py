import psycopg2

# Database connection parameters
dbname = "postgres"
user = "youssefbr"
password = ""
host = "localhost"
port = "5432"

# Connection string
conn_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"

# Globals
in_transaction = False
sql_query = ""

def generate_insert_sql(table, data):
    global sql_query
    columns = ', '.join(data.keys())
    values = ', '.join([f"{v}" for v in data.values()])
    sql_query += f"INSERT INTO {table} ({columns}) VALUES ({values});\n"

def generate_update_sql(table, conditions, data):
    global sql_query
    set_clause = ', '.join([f"{k} = {v}" for k, v in data.items()])
    sql_query += f"UPDATE {table} SET {set_clause}"
    if conditions != "":
        sql_query += f" WHERE {conditions}"
    sql_query += ";\n"

def generate_delete_sql(table, conditions):
    global sql_query
    sql_query += f"DELETE FROM {table}"
    if conditions != "":
        sql_query += f" WHERE {conditions}"
    sql_query += ";\n"

def generate_search_sql(table, columns, conditions):
    global sql_query
    select_clause = columns if columns else '*'
    sql_query += f"SELECT {select_clause} FROM {table}"
    if conditions != "":
        sql_query += f" WHERE {conditions};\n"
    sql_query += ";\n"

def generate_aggregate_sql(table):
    global sql_query
    select_clause = input("Enter an aggregate function (e.g., SUM(column_name), AVG(column_name), ...): ").strip()
    sql_query += f"SELECT {select_clause} FROM {table};\n"

def generate_sorting_sql(table, columns, conditions):
    global sql_query
    select_clause = columns if columns else '*'
    sql_query += f"SELECT {select_clause} FROM {table}"
    if conditions != "":
        sql_query += f" WHERE {conditions}"
    order_by_column = input("Enter a column to sort by and a direction (format: column_name ASC/DESC): ").strip()
    sql_query += f" ORDER BY {order_by_column};\n"

def generate_join_sql():
    global sql_query
    table1 = input("Enter the first table name: ").strip().lower()
    table2 = input("Enter the second table name: ").strip().lower()
    join_type = input("Enter the join type: ").strip().upper()
    join_condition = input("Enter the join condition: ").strip().lower()
    sql_query += f"SELECT * FROM {table1} {join_type} {table2} ON {join_condition};\n"

def generate_grouping_sql(table):
    global sql_query
    select_clause = input("Enter a column followed by a aggregate function (format: column_name(s), AGGREGATE(column_name)):").strip()
    group_by_column = input("Enter a column to group by: ").strip()
    sql_query += f"SELECT {select_clause} FROM {table} GROUP BY {group_by_column};\n"

def generate_subquery_sql(table):
    global sql_query
    subquery_table = input("Enter the subquery table name: ").strip().lower()
    column = input("Enter the column to search for in the subquery table: ").strip().lower()
    sql_query += f"SELECT * FROM {table} WHERE {column} IN (SELECT {column} FROM {subquery_table});\n"

def default_case():
    return "Oops! Unrecognized command."

def parse_key_value_to_dict(input_string):
    pairs = input_string.split(',')
    result = {}
    for pair in pairs:
        key, value = pair.strip().split('=')
        result[key] = value
    return result

def start_transaction():
    global in_transaction
    global sql_query
    in_transaction = True
    sql_query = "BEGIN TRANSACTION;\n"
    print("Transaction started.")

def end_transaction():
    global in_transaction
    global sql_query
    in_transaction = False
    ending = int(input("Select an option:\n 1. Commit\n 2. Rollback\n"))
    sql_query += "COMMIT;\n" if ending == 1 else "ROLLBACK;\n"
    print("Transaction ended.")

def to_int(user_in):
    int_version = -1
    try:
        int_version = int(user_in)
    except ValueError:
        print("Please enter a valid integer.")
    return int_version


# Input mapping to functions
option_num_to_str = {
    1: 'insert',
    2: 'update',
    3: 'delete',
    4: 'search',
    5: 'aggregate_fns',
    6: 'sorting',
    7: 'join',
    8: 'grouping',
    9: 'subquery'
}

def main():

    # Connect to the database
    conn = psycopg2.connect(conn_string)
    conn.autocommit = False
    print("Connected to the database.")

    # Cursor object necessary to get results and interact with database
    cursor = conn.cursor()

    global sql_query
    global in_transaction

    while True:

        option = 0
        if in_transaction:
            option = to_int(input("Select an option:\n 1. SQL Command\n 2. End transaction\n 3. Quit\n"))
            if(option == 2):
                end_transaction()
                continue
        else:
            option = to_int(input("Select an option:\n 1. SQL Command\n 2. Start transaction\n 3. Quit\n"))
            if(option == 2):
                start_transaction()
                continue
        
        if(option == -1): continue
        elif(option == 3):
            break
        elif(option != 1):
            print(default_case())
            continue
    
        action = to_int(input("Select an action:\n 1. Insert\n 2. Update\n 3. Delete\n 4. Search\n 5. Aggregate Functions\n 6. Sorting\n 7. Joins\n 8. Grouping\n 9. Subqueries\n"))

        if(action == -1): continue
        elif(action < 1 or action > 9):
            print(default_case())
            continue

        action = option_num_to_str[action]
        
        if(action != 'join'): table = input("Enter table name: ").strip().lower()
        
        data = {}
        columns = ""
        
        if action in ['insert', 'update']:
            data_input = input(f"Enter data to {action} (format: key1=value1,key2=value2,...): ")
            data = parse_key_value_to_dict(data_input)
        elif action in ['search', 'sorting']:
            columns = input("Enter columns to select (comma-separated, empty for all): ").strip().lower()

        conditions = ""
        if action in ['update', 'delete', 'search', 'sorting']:
            conditions = input("Enter conditions (empty for no conditions): ").strip().lower()

        if action == "insert":
            generate_insert_sql(table, data)
        elif action == "update":
            generate_update_sql(table, conditions, data)
        elif action == "delete":
            generate_delete_sql(table, conditions)
        elif action == "search":
            generate_search_sql(table, columns, conditions)
        elif action == "aggregate_fns":
            generate_aggregate_sql(table)
        elif action == "sorting":
            generate_sorting_sql(table, columns, conditions)
        elif action == "join":
            generate_join_sql()
        elif action == "grouping": 
            generate_grouping_sql(table)
        else:
            generate_subquery_sql(table)

        try:
            
            cursor.execute(sql_query)

            # Fetch and print the result of the query
            if action not in ['insert', 'update', 'delete']:
                records = cursor.fetchall()
                for record in records:
                    print(record)
            
            print(sql_query)
            
            # Only need to commit a change if a change causing command was executed
            if not in_transaction:
                conn.commit()
                sql_query = ""

        except Exception as e:
            print("You provided an invalid query:\n{sql_query}", e)
            conn.rollback()
            sql_query = ""

    # Cleanup of open objects to end cleanly
    cursor.close()
    if conn:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()