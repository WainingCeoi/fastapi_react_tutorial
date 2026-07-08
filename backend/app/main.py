from fastapi import FastAPI      # import the framework's main class

app = FastAPI()                  # create THE application object. Remember the name "app".


@app.get("/")                    # register: "when an HTTP GET arrives for path '/', run the function below"
def read_root():                 # a plain Python function — the "handler" for that route
    return {"message": "Hello, world"}   # return a dict; FastAPI auto-converts it to a JSON response