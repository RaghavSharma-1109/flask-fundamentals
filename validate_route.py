from dotenv import load_dotenv
load_dotenv()
from app_factory import create_app
from config import Config

app= create_app()
app.config.from_object(Config)

if __name__=="__main__":
    app.run(debug=True) 