from fastapi import FastAPI, HTTPException, Path
import json
app = FastAPI()


def load_data():
    with open('expenses.json','r') as f:
        data = json.load(f)
    return data

@app.get("/hello")
def hello():
    return "Hi"


@app.get("/about")
def about():
    return "This is our about page."


@app.get("/view")
def view_expenses():
    data = load_data()
    return data


@app.get("/view/{expense_id}")
def view_specific_expense(expense_id: str = Path(..., description='ID of the expense', example='E001')):
    data = load_data()
    if expense_id in data:
        return data[expense_id]
    else:
        raise HTTPException(status_code=404, detail='Expense not found.')


@app.get("/sort")
def view_sorted_expenses(sorted_by : str, order : str):
    data = load_data()

    sorted_data = list(data.values())
    def get_value(expense):
        return expense[sorted_by]
    if order == 'asc':
        sorted_data.sort(key = get_value)
    else:
        sorted_data.sort(key = get_value, reverse=True)
    return sorted_data