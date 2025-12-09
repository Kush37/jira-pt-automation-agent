import os
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables (ensure OPENAI_API_KEY is available)
load_dotenv()

# Define the output structure we want
class LoadTestScenario(BaseModel):
    concurrent_users: Optional[int] = Field(description="Number of concurrent users / VUs")
    test_duration: Optional[int] = Field(description="Duration of the test in Minutes (e.g., '60', '30')")
    ramp_up_duration: Optional[int] = Field(description="Ramp-up period duration in Minutes (e.g., '10', '20')")
    ramp_down_duration: Optional[int] = Field(description="Ramp-down period duration in Minutes (e.g., '10', '20')")
    target_tph: Optional[int] = Field(description="Target Transactions Per Hour (TPH) in Minutes (e.g., '10', '1000', '2000')")

def create_scenario_from_story(jira_story: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes a Jira story to extract load testing scenario parameters using an LLM.
    
    Args:
        jira_story (Dict[str, Any]): A dictionary containing Jira story details 
                                     (title, description, comments, etc.)
                                     
    Returns:
        Dict[str, Any]: Extracted scenario parameters.
    """
    
    # Check if API key is present
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "status": "error",
            "message": "OPENAI_API_KEY not found in environment variables."
        }

    try:
        # Initialize the model
        # Using a temperature of 0 for deterministic extraction
        model = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Set up the parser
        parser = PydanticOutputParser(pydantic_object=LoadTestScenario)
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a QA Performance Testing expert. Your goal is to extract load testing parameters from a JIRA story."),
            ("user", """
            Analyze the following JIRA user story and extract the performance testing requirements.
            
            Look for these specific details in the Description, Comments, or Title:
            1. Concurrent Users (VUs)
            2. Test Duration
            3. Ramp Up Duration
            4. Ramp Down Duration
            5. Target TPH (Transactions Per Hour)
            
            If a value is not explicitly stated but can be reasonably inferred (e.g., "ramp up over 5 mins"), extract it.
            If a value is completely missing, return -1 for that field.
            
            JIRA Story Details:
            Title: {title}
            Description: {description}
            Comments: {comments}
            
            {format_instructions}
            """)
        ])
        
        # Chain the components
        chain = prompt | model | parser
        
        # Prepare input
        story_input = {
            "title": jira_story.get("title", ""),
            "description": jira_story.get("description", ""),
            "comments": str(jira_story.get("comments", [])),
            "format_instructions": parser.get_format_instructions()
        }
        
        # Execute
        scenario: LoadTestScenario = chain.invoke(story_input)
        
        res = {
            "status": "success",
            "data": scenario.dict(),
            "message": "Load details captured from story."
        }
        print(res)
        return res
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to extract scenario: {str(e)}"
        }

# Optional: Simple test block if run directly
if __name__ == "__main__":
    sample_story = {
        "title": "Load Test for Payment API",
        "description": "We need to verify the system handles 500 concurrent users for a duration of 1 hour. Ramp up should be 10 minutes. Target 20000 TPH.",
        "comments": ["Also, ensure we have a 5 minute ramp down period."]
    }
    result = create_scenario_from_story(sample_story)
    print("Extraction Result:", result)
