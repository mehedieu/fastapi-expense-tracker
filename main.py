from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel,Field
import json
app = FastAPI()

class Expense(BaseModel):
    id: str
    name: str
    amount: int
    category: str
    date: str
    description: str

class ExpenseUpdate(BaseModel):
    name: str | None = None
    amount: int | None = None
    category: str | None = None
    date: str | None = None
    description: str | None = None


def load_data():
    with open('expenses.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('expenses.json','w') as f:
        json.dump(data, f)



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
def view_specific_expense(expense_id: str = Path(..., description='ID of the expense', examples='E001')):
    data = load_data()
    if expense_id in data:
        return data[expense_id]
    else:
        raise HTTPException(status_code=404, detail='Expense not found.')


@app.get("/sort")
def view_sorted_expenses(sorted_by : str,order : str):
    data = load_data()

    sorted_data = list(data.values())
   # sorted_data.sort(key=lambda x:x[sorted_by])


    def get_value(expense):
        return expense[sorted_by]
    if order == 'asc':
        sorted_data.sort(key = get_value)
    else:
        sorted_data.sort(key = get_value, reverse=True)

    return sorted_data


@app.post("/create")
def create_expense(expense: Expense):
    data = load_data()
    if expense.id in data:
        raise HTTPException(status_code=400, detail='Expense id already exists.')
    data[expense.id] = expense.model_dump(exclude=['id'])
    save_data(data)

@app.put("/edit/{expense_id}")
def update_expense(expense_id : str, expense: ExpenseUpdate):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail='Expense not found')
    data[expense_id].update(expense.model_dump(exclude_unset = True))
    save_data(data)


@app.delete("/delete/{expense_id}")
def delete_expense(expense_id : str):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail='Expense not found')
    del data[expense_id]
    save_data(data)
