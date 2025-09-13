import os
from dotenv import load_dotenv
from search import search_prompt
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm():
    """Returns the LLM instance based on environment variables"""
    # Check if OpenAI API key is available
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model=os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini"),
            temperature=0
        )
    # Check if Google API key is available
    elif os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.0-flash-exp"),
            temperature=0
        )
    else:
        raise ValueError("No API key configured. Set OPENAI_API_KEY or GOOGLE_API_KEY")

def check_system_initialization():
    """Checks if the system is working correctly"""
    try:
        # Test if search_prompt works correctly
        test_prompt = search_prompt("test")
        if not test_prompt:
            return False, "Error in search function"
        return True, "System initialized successfully"
    except Exception as e:
        return False, f"Initialization error: {str(e)}"

def main():
    try:
        # Initialize the LLM
        llm = get_llm()
        
        # Check if the system is working
        is_ready, message = check_system_initialization()
        if not is_ready:
            print(f"Could not start chat. {message}")
            return
        
        print("🤖 Chat started! Type 'sair' to exit.\n")
        
        while True:
            # Request user question
            question = input("Question: ").strip()
            
            # Check if user wants to exit
            if question.lower() in ['sair', 'exit', 'quit']:
                print("Goodbye!")
                break
            
            # Check if question is not empty
            if not question:
                print("Please enter a valid question.\n")
                continue
            
            try:
                # Search for relevant context and build prompt
                prompt = search_prompt(question)
                
                # Call LLM with the prompt
                response = llm.invoke(prompt)
                
                # Display the response
                print(f"ANSWER: {response.content}\n")
                
            except Exception as e:
                print(f"Error processing question: {str(e)}\n")
                
    except Exception as e:
        print(f"Error starting chat: {str(e)}")
        print("Check if environment variables are configured correctly.")

if __name__ == "__main__":
    main()