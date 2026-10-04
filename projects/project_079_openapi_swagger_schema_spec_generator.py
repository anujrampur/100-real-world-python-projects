# Project 79: OpenAPI / Swagger Schema Spec Generator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import inspect
import json
import tkinter as tk
from tkinter import messagebox


# Sample API Endpoints to document
def get_users():
    """Summary: Fetch all registered users
    Method: GET
    Path: /users
    Response: 200 OK array of user objects"""
    pass


def create_user(username: str, age: int):
    """Summary: Create a new user profile
    Method: POST
    Path: /users
    Response: 201 Created"""
    pass


def delete_user(user_id: int):
    """Summary: Delete a user by ID
    Method: DELETE
    Path: /users/{id}
    Response: 204 No Content"""
    pass


def generate_openapi_spec(endpoints):
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "Auto-Generated REST API", "version": "1.0.0"},
        "paths": {},
    }
    for func in endpoints:
        doc = inspect.getdoc(func) or ""
        lines = [line.strip() for line in doc.split("\n") if line.strip()]
        doc_dict = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                doc_dict[k.strip().lower()] = v.strip()
        path = doc_dict.get("path", f"/{func.__name__}")
        method = doc_dict.get("method", "GET").lower()
        summary = doc_dict.get("summary", "No summary provided.")
        if path not in spec["paths"]:
            spec["paths"][path] = {}
        spec["paths"][path][method] = {
            "summary": summary,
            "operationId": func.__name__,
            "responses": {
                "200": {"description": doc_dict.get("response", "Success")}
            },
        }
    return json.dumps(spec, indent=4)


def run_generator():
    spec_json = generate_openapi_spec([get_users, create_user, delete_user])
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, spec_json)


root = tk.Tk()
root.title("OpenAPI 3.0 Spec Generator")
root.geometry("560x440")
tk.Label(
    root,
    text="OPENAPI / SWAGGER SPEC GENERATOR",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
tk.Button(
    root,
    text="Introspect Code & Generate OpenAPI JSON",
    command=run_generator,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
).pack(pady=6)
output_text = tk.Text(
    root, height=16, width=62, font=("Consolas", 9), bg="#f8fafc"
)
output_text.pack(padx=20, pady=10)
run_generator()
root.mainloop()
