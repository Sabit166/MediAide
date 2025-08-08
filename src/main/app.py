"""
MediAide - AI-Powered Medical Assistant
Main application file that orchestrates all medical tools and agents.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List
import logging
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd
from pyprojroot import here

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv()

# Import tools
try:
    from src.tool.DiabetesDBTool import diabetes_db_tool
    from src.tool.CancerDBTool import cancer_db_tool
    from src.tool.HeartDiseaseDBTool import heart_disease_db_tool
    from src.tool.MedicalWebSearchTool import web_search
except ImportError as e:
    print(f"⚠️ Warning: Could not import some tools: {e}")

# Import settings
try:
    from src.main import settings
except ImportError:
    print("⚠️ Settings not found. Make sure to configure your LLM settings.")
    settings = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
    df.to_sql("diabetes", engine, index=False, if_exists='replace')
    print("Database created and data loaded into 'diabetes' table.")
    db = SQLDatabase(engine=engine)
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM diabetes WHERE Age < 2;")
    print("Query executed successfully.")
    return db


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
    df.to_sql("cancer", engine, index=False, if_exists='replace')
    print("Database created and data loaded into 'cancer' table.")
    db = SQLDatabase(engine=engine)
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM cancer WHERE Age < 2;")
    print("Query executed successfully.")
    return db


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
    df.to_sql("heart_disease", engine, index=False, if_exists='replace')
    print("Database created and data loaded into 'heart_disease' table.")
    db = SQLDatabase(engine=engine)
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM heart_disease WHERE Age < 2;")
    print("Query executed successfully.")
    return db


class MediAide:
    """
    Main MediAide application class that coordinates all medical tools and agents.
    """
    
    def __init__(self):
        """Initialize the MediAide application."""
        self.tools = {
            'diabetes': None,
            'cancer': None,
            'heart_disease': None,
            'web_search': None
        }
        self.initialized = False
        
    def initialize(self) -> bool:
        """
        Initialize all medical tools and agents.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing MediAide application...")
            
            # Initialize database creation functions
            try:
                get_diabetes_db()
                get_cancer_db()
                get_heart_disease_db()
                logger.info("✅ Databases created/updated successfully")
            except Exception as e:
                logger.warning(f"⚠️ Database creation warning: {e}")
            
            # Initialize database tools
            try:
                if 'diabetes_db_tool' in globals():
                    self.tools['diabetes'] = diabetes_db_tool
                if 'cancer_db_tool' in globals():
                    self.tools['cancer'] = cancer_db_tool
                if 'heart_disease_db_tool' in globals():
                    self.tools['heart_disease'] = heart_disease_db_tool
                logger.info("✅ Database tools initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Database tools warning: {e}")
            
            # Initialize web search tool
            try:
                if 'web_search' in globals():
                    self.tools['web_search'] = web_search
                    logger.info("✅ Web search tool initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Web search tool warning: {e}")
            
            self.initialized = True
            logger.info("🚀 MediAide application initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize MediAide: {e}")
            return False
    
    def query_diabetes(self, question: str) -> Dict[str, Any]:
        """
        Query the diabetes database agent.
        
        Args:
            question (str): The question about diabetes
            
        Returns:
            Dict[str, Any]: Response with answer and metadata
        """
        try:
            if not self.tools['diabetes']:
                return {
                    "answer": "Diabetes database tool not available. Please check your configuration.",
                    "source": "error",
                    "success": False
                }
            
            agent = self.tools['diabetes']()
            response = agent.invoke({"input": question})
            
            return {
                "answer": response.get('output', response),
                "source": "diabetes_database",
                "success": True,
                "metadata": {
                    "tool_used": "diabetes_db_agent",
                    "question": question
                }
            }
            
        except Exception as e:
            logger.error(f"Error querying diabetes database: {e}")
            return {
                "answer": f"Error occurred while querying diabetes database: {str(e)}",
                "source": "error",
                "success": False
            }
    
    def query_cancer(self, question: str) -> Dict[str, Any]:
        """
        Query the cancer database agent.
        
        Args:
            question (str): The question about cancer
            
        Returns:
            Dict[str, Any]: Response with answer and metadata
        """
        try:
            if not self.tools['cancer']:
                return {
                    "answer": "Cancer database tool not available. Please check your configuration.",
                    "source": "error",
                    "success": False
                }
            
            agent = self.tools['cancer']()
            response = agent.invoke({"input": question})
            
            return {
                "answer": response.get('output', response),
                "source": "cancer_database",
                "success": True,
                "metadata": {
                    "tool_used": "cancer_db_agent",
                    "question": question
                }
            }
            
        except Exception as e:
            logger.error(f"Error querying cancer database: {e}")
            return {
                "answer": f"Error occurred while querying cancer database: {str(e)}",
                "source": "error",
                "success": False
            }
    
    def query_heart_disease(self, question: str) -> Dict[str, Any]:
        """
        Query the heart disease database agent.
        
        Args:
            question (str): The question about heart disease
            
        Returns:
            Dict[str, Any]: Response with answer and metadata
        """
        try:
            if not self.tools['heart_disease']:
                return {
                    "answer": "Heart disease database tool not available. Please check your configuration.",
                    "source": "error",
                    "success": False
                }
            
            agent = self.tools['heart_disease']()
            response = agent.invoke({"input": question})
            
            return {
                "answer": response.get('output', response),
                "source": "heart_disease_database",
                "success": True,
                "metadata": {
                    "tool_used": "heart_disease_db_agent",
                    "question": question
                }
            }
            
        except Exception as e:
            logger.error(f"Error querying heart disease database: {e}")
            return {
                "answer": f"Error occurred while querying heart disease database: {str(e)}",
                "source": "error",
                "success": False
            }
    
    def search_web(self, question: str) -> Dict[str, Any]:
        """
        Search the web for medical information.
        
        Args:
            question (str): The medical question to search for
            
        Returns:
            Dict[str, Any]: Response with search results and metadata
        """
        try:
            if not self.tools['web_search']:
                return {
                    "answer": "Web search tool not available. Please check your configuration.",
                    "source": "error",
                    "success": False
                }
            
            results = self.tools['web_search'](question)
            
            return {
                "answer": results,
                "source": "web_search",
                "success": True,
                "metadata": {
                    "tool_used": "medical_web_search",
                    "question": question
                }
            }
            
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return {
                "answer": f"Error occurred while searching the web: {str(e)}",
                "source": "error",
                "success": False
            }
    
    def get_comprehensive_answer(self, question: str, topics: List[str] = None) -> Dict[str, Any]:
        """
        Get a comprehensive answer by querying multiple sources.
        
        Args:
            question (str): The medical question
            topics (List[str]): List of topics to search ('diabetes', 'cancer', 'heart_disease', 'web')
            
        Returns:
            Dict[str, Any]: Comprehensive response from multiple sources
        """
        if not topics:
            topics = ['diabetes', 'cancer', 'heart_disease', 'web']
        
        responses = {}
        
        if 'diabetes' in topics:
            responses['diabetes'] = self.query_diabetes(question)
        
        if 'cancer' in topics:
            responses['cancer'] = self.query_cancer(question)
        
        if 'heart_disease' in topics:
            responses['heart_disease'] = self.query_heart_disease(question)
        
        if 'web' in topics:
            responses['web_search'] = self.search_web(question)
        
        return {
            "question": question,
            "responses": responses,
            "comprehensive": True,
            "sources": list(responses.keys())
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of all tools and services.
        
        Returns:
            Dict[str, Any]: Status information
        """
        status = {
            "initialized": self.initialized,
            "tools": {
                "diabetes_db": self.tools['diabetes'] is not None,
                "cancer_db": self.tools['cancer'] is not None,
                "heart_disease_db": self.tools['heart_disease'] is not None,
                "web_search": self.tools['web_search'] is not None
            },
            "environment": {
                "settings_loaded": settings is not None,
                "llm_configured": settings and hasattr(settings, 'llm') if settings else False
            }
        }
        
        return status


def test_databases():
    """
    Test function to create and verify databases.
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

    print("All database tests completed.")


def main():
    """Main function to run the MediAide application."""
    print("🏥 Welcome to MediAide - AI-Powered Medical Assistant")
    print("=" * 60)
    
    # Initialize the application
    app = MediAide()
    if not app.initialize():
        print("❌ Failed to initialize MediAide. Please check your configuration.")
        return
    
    # Show status
    status = app.get_status()
    print("\n📊 System Status:")
    print(f"  • Initialized: {status['initialized']}")
    print(f"  • Diabetes DB: {'✅' if status['tools']['diabetes_db'] else '❌'}")
    print(f"  • Cancer DB: {'✅' if status['tools']['cancer_db'] else '❌'}")
    print(f"  • Heart Disease DB: {'✅' if status['tools']['heart_disease_db'] else '❌'}")
    print(f"  • Web Search: {'✅' if status['tools']['web_search'] else '❌'}")
    
    # Interactive mode
    print("\n🤖 Interactive Mode - Ask medical questions or type 'quit' to exit")
    print("Available commands:")
    print("  • 'diabetes: <question>' - Query diabetes database")
    print("  • 'cancer: <question>' - Query cancer database")
    print("  • 'heart: <question>' - Query heart disease database")
    print("  • 'search: <question>' - Search web for medical info")
    print("  • 'all: <question>' - Query all sources")
    print("  • 'test' - Test database creation")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n💬 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thank you for using MediAide!")
                break
            
            if user_input.lower() == 'test':
                test_databases()
                continue
            
            if not user_input:
                continue
            
            # Parse command
            if ':' in user_input:
                command, question = user_input.split(':', 1)
                command = command.strip().lower()
                question = question.strip()
            else:
                command = 'search'
                question = user_input
            
            print(f"\n🔍 Processing: {question}")
            
            # Route to appropriate handler
            if command == 'diabetes':
                response = app.query_diabetes(question)
            elif command == 'cancer':
                response = app.query_cancer(question)
            elif command in ['heart', 'heart_disease']:
                response = app.query_heart_disease(question)
            elif command == 'search':
                response = app.search_web(question)
            elif command == 'all':
                response = app.get_comprehensive_answer(question)
                print("\n📋 Comprehensive Results:")
                for source, result in response['responses'].items():
                    print(f"\n🔸 {source.upper()}:")
                    print(f"   {result['answer'][:200]}...")
                continue
            else:
                print(f"❓ Unknown command: {command}")
                continue
            
            # Display response
            print(f"\n💡 Answer ({response['source']}):")
            print(f"   {response['answer']}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using MediAide!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
