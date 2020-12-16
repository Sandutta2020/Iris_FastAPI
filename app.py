from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Model import IrisModel, IrisSpecies

from pydantic import BaseModel
import random
import uvicorn

# initialization
app = FastAPI()
model = IrisModel()

# mount static folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template instance for returning webpage via template engine
templates = Jinja2Templates(directory="templates")

# serve webpage, GET method, return HTML
@app.get("/", response_class=HTMLResponse)
async def get_webpage(request: Request):
    return templates.TemplateResponse(
        "form.html", {"request": request, "message": "Contact Us"}
    )


@app.post("/render", response_class=HTMLResponse)
async def render(
    request: Request,
    sepal_length: float = Form(...),
    sepal_width: float = Form(...),
    petal_length: float = Form(...),
    petal_width: float = Form(...),
):
    prediction, probability = model.predict_species(
        sepal_length, sepal_width, petal_length, petal_width
    )
    return templates.TemplateResponse(
        "form.html",
        context={
            "request": request,
            "Res": {"prediction": prediction, "probability": probability},
            "sepal_length": petal_length,
            "sepal_width": sepal_width,
            "petal_length": sepal_length,
            "petal_width": petal_width,
        },
    )


# main
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
