from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd
from pyprojroot import here


def get_diabetes_db():
    """
    Returns a SQLDatabase object connected to the diabetes database.
    """
    
    df = pd.read_csv(here("src/data/diabetes.csv"))
    #print(df.shape)
    #print(df.columns.tolist())
    #display(df.head(3))

    db_path = str(here("src/database")) + "/diabetes.db"
    db_path = f"sqlite:///{db_path}"

    engine = create_engine(db_path)
    df.to_sql("diabetes", engine, index=False)
    print("Database created and data loaded into 'diabetes' table.")
    db = SQLDatabase(engine=engine)
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM diabetes WHERE Age < 2;")
    print("Query executed successfully.")


def get_cancer_db():
    """
    Returns a SQLDatabase object connected to the cancer database.
    """
    
    df = pd.read_csv(here("src/data/The_Cancer_data_1500_V2.csv"))
    #print(df.shape)
    #print(df.columns.tolist())
    #display(df.head(3))
    
    db_path = str(here("src/database")) + "/cancer.db"
    db_path = f"sqlite:///{db_path}"

    engine = create_engine(db_path)
    df.to_sql("cancer", engine, index=False)
    print("Database created and data loaded into 'cancer' table.")
    db = SQLDatabase(engine=engine)
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM cancer WHERE Age < 2;")
    print("Query executed successfully.")


def get_heart_disease_db():
    """
    Returns a SQLDatabase object connected to the heart disease database.
    """
    
    df = pd.read_csv(here("src/data/heart.csv"))
    #print(df.shape)
    #print(df.columns.tolist())
    #display(df.head(3))

    db_path = str(here("src/database")) + "/heart_disease.db"
    db_path = f"sqlite:///{db_path}"

    engine = create_engine(db_path)
    df.to_sql("heart_disease", engine, index=False)
    print("Database created and data loaded into 'heart_disease' table.")
    db = SQLDatabase(engine=engine)
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM heart_disease WHERE Age < 2;")
    print("Query executed successfully.")
    
def main():
    """
    Main function to test the database connection functions.
    """
    print("Testing diabetes database...")
    try:
        get_diabetes_db()
        print("Diabetes database test PASSED\n")
    except Exception as e:
        print(f"Diabetes database test FAILED: {str(e)}\n")

    print("Testing cancer database...")
    try:
        get_cancer_db()
        print("Cancer database test PASSED\n")
    except Exception as e:
        print(f"Cancer database test FAILED: {str(e)}\n")

    print("Testing heart disease database...")
    try:
        get_heart_disease_db()
        print("Heart disease database test PASSED\n")
    except Exception as e:
        print(f"Heart disease database test FAILED: {str(e)}\n")

    print("All tests completed.")

if __name__ == "__main__":
    main()
