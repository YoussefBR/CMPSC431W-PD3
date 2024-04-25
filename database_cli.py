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

def generate_insert_sql(table: str, data: dict) -> None:
    """
    Generates an SQL INSERT statement for a specific table and data.
    
    Parameters:
        table (str): The name of the table to insert data into.
        data (dict): A dictionary where keys are column names and values are the data to be inserted.
        
    Returns:
        None: Modifies the global sql_query variable by appending the generated INSERT statement.
    """
    global sql_query
    columns = ', '.join(data.keys())
    values = ', '.join([f"{v}" for v in data.values()])
    sql_query += f"INSERT INTO {table} ({columns}) VALUES ({values});\n"

def generate_update_sql(table: str, conditions: str, data: dict) -> None:
    """
    Generates an SQL UPDATE statement for a specific table, conditions, and data.
    
    Parameters:
        table (str): The name of the table to update.
        conditions (str): The WHERE clause specifying which records to update.
        data (dict): A dictionary where keys are column names and values are the new data for these columns.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated UPDATE statement.
    """
    global sql_query
    set_clause = ', '.join([f"{k} = {v}" for k, v in data.items()])
    sql_query += f"UPDATE {table} SET {set_clause}"
    if conditions != "":
        sql_query += f" WHERE {conditions}"
    sql_query += ";\n"

def generate_delete_sql(table: str, conditions: str) -> None:
    """
    Generates an SQL DELETE statement for a specific table based on conditions.
    
    Parameters:
        table (str): The name of the table to delete data from.
        conditions (str): The WHERE clause specifying which records to delete.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated DELETE statement.
    """
    global sql_query
    sql_query += f"DELETE FROM {table}"
    if conditions != "":
        sql_query += f" WHERE {conditions}"
    sql_query += ";\n"

def generate_search_sql(table: str, columns: str, conditions: str) -> None:
    """
    Generates an SQL SELECT statement for searching data in a specific table based on optional columns and conditions.
    
    Parameters:
        table (str): The name of the table to search.
        columns (str): A string of comma-separated column names to retrieve (defaults to '*').
        conditions (str): The WHERE clause specifying the conditions of the search.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated SELECT statement.
    """
    global sql_query
    select_clause = columns if columns else '*'
    sql_query += f"SELECT {select_clause} FROM {table}"
    if conditions != "":
        sql_query += f" WHERE {conditions};\n"
    sql_query += ";\n"

def generate_aggregate_sql(table: str) -> None:
    """
    Prompts the user to input an aggregate function and then generates an SQL SELECT statement
    to execute that function on a specific table.
    
    Parameters:
        table (str): The name of the table to perform the aggregation on.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated SELECT statement.
    """
    global sql_query
    select_clause = input("Enter an aggregate function (e.g., SUM(column_name), AVG(column_name), ...): ").strip()
    sql_query += f"SELECT {select_clause} FROM {table};\n"

def generate_sorting_sql(table: str, columns: str, conditions: str) -> None:
    """
    Generates an SQL SELECT statement that sorts the results from a specific table based on user-defined criteria.
    
    Parameters:
        table (str): The name of the table to sort data from.
        columns (str): Columns to include in the output (comma-separated, '*' for all columns).
        conditions (str): The WHERE clause specifying the conditions of the search.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated SELECT statement with an ORDER BY clause.
    """
    global sql_query
    select_clause = columns if columns else '*'
    sql_query += f"SELECT {select_clause} FROM {table}"
    if conditions != "":
        sql_query += f" WHERE {conditions}"
    order_by_column = input("Enter a column to sort by and a direction (format: column_name ASC/DESC): ").strip()
    sql_query += f" ORDER BY {order_by_column};\n"

def generate_join_sql() -> None:
    """
    Generates an SQL SELECT statement that performs a join operation based on user inputs.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated SELECT statement for the join.
    """
    global sql_query
    table1 = input("Enter the first table name: ").strip().lower()
    table2 = input("Enter the second table name: ").strip().lower()
    join_type = input("Enter the join type: ").strip().upper()
    join_condition = input("Enter the join condition: ").strip().lower()
    sql_query += f"SELECT * FROM {table1} {join_type} {table2} ON {join_condition};\n"

def generate_grouping_sql(table: str) -> None:
    """
    Prompts the user to specify grouping columns and an optional HAVING clause, and generates
    an SQL SELECT statement that groups the results from a specified table.
    
    Parameters:
        table (str): The name of the table to group data from.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated GROUP BY statement.
    """
    global sql_query
    select_clause = input("Enter a column followed by a aggregate function (format: column_name(s), AGGREGATE(column_name)):").strip()
    group_by_column = input("Enter a column to group by: ").strip()
    sql_query += f"SELECT {select_clause} FROM {table} GROUP BY {group_by_column};\n"

def generate_subquery_sql(table: str) -> None:
    """
    Generates an SQL SELECT statement that includes a subquery. The user must manually specify the complete
    subquery within the SELECT statement.
    
    Parameters:
        table (str): The name of the table to include in the outer query of the subquery.
    
    Returns:
        None: Modifies the global sql_query variable by appending the generated SELECT statement with a subquery.
    """
    global sql_query
    subquery_table = input("Enter the subquery table name: ").strip().lower()
    column = input("Enter the column to search for in the subquery table: ").strip().lower()
    sql_query += f"SELECT * FROM {table} WHERE {column} IN (SELECT {column} FROM {subquery_table});\n"

def default_case() -> str:
    """
    Default case for unrecognized commands.

    Returns:
        str: The error message.
    """
    return "Oops! Unrecognized command."

def parse_key_value_to_dict(input_string: str) -> dict:
    """
    Parses a string of key-value pairs into a dictionary. The expected format is key=value pairs separated by commas.
    
    Parameters:
        data_input (str): The input string containing key-value pairs.
    
    Returns:
        dict: A dictionary where each key is a column name and each value is the corresponding data entry.
    """
    pairs = input_string.split(',')
    result = {}
    for pair in pairs:
        key, value = pair.strip().split('=')
        result[key] = value
    return result

def start_transaction() -> None:
    """
    Starts a transaction by setting the proper global variables.

    Returns:
        None: Modifies the global in_transaction and sql_query variables.
    """
    global in_transaction
    global sql_query
    in_transaction = True
    sql_query = "BEGIN TRANSACTION;\n"
    print("Transaction started.")

def end_transaction() -> None:
    """
    Ends a transaction by setting the proper global variables and prompting the user to commit or rollback.

    Returns:
        None: Modifies the global in_transaction and sql_query variables.
    """
    global in_transaction
    global sql_query
    in_transaction = False
    ending = int(input("Select an option:\n 1. Commit\n 2. Rollback\n"))
    sql_query += "COMMIT;\n" if ending == 1 else "ROLLBACK;\n"
    print("Transaction ended.")

def to_int(user_in: str) -> int:
    """
    Convert user input to an integer. If the input is not a valid integer print an error message. Prevents program from crashing on invalid user input.

    Parameters:
        user_in (str): User input to convert to an integer.

    Returns:
        int: The integer version of the user input or -1 if the input is not a valid integer.
    """
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
    """
    Main function to handle database operations based on user inputs. It establishes a database connection,
    executes SQL queries based on the specified action, and handles exceptions and transaction management.
    """
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
                cursor.execute(sql_query)
                continue
        else:
            option = to_int(input("Select an option:\n 1. SQL Command\n 2. Start transaction\n 3. Quit\n"))
            if(option == 2):
                start_transaction()
                continue
        
        # If the input is not valid, easiest just to re-prompt from the beginning
        if(option == -1): continue
        elif(option == 3):
            break # Only exit point
        elif(option != 1):
            print(default_case())
            continue
    
        action = to_int(input("Select an action:\n 1. Insert\n 2. Update\n 3. Delete\n 4. Search\n 5. Aggregate Functions\n 6. Sorting\n 7. Joins\n 8. Grouping\n 9. Subqueries\n"))

        if(action == -1): continue
        elif(action < 1 or action > 9):
            print(default_case())
            continue

        action = option_num_to_str[action]
        
        # JOIN requires two tables, so table request will be worded slightly different to avoid confusion
        if(action != 'join'): table = input("Enter table name: ").strip().lower()
        
        data = {}
        columns = ""
        
        # Data is only needed for INSERT and UPDATE
        if action in ['insert', 'update']:
            data_input = input(f"Enter data to {action} (format: key1=value1,key2=value2,...): ")
            data = parse_key_value_to_dict(data_input)
        elif action in ['search', 'sorting']:
            columns = input("Enter columns to select (comma-separated, empty for all): ").strip().lower()

        # Conditions are only needed for UPDATE, DELETE, SEARCH, and SORTING
        conditions = ""
        if action in ['update', 'delete', 'search', 'sorting']:
            conditions = input("Enter conditions (empty for no conditions): ").strip().lower()

        # Each type of query is associated with a unique function
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