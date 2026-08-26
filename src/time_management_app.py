from flask import Flask, request, jsonify, abort
from src.data.queries import (
    list_persons, find_person_by_id, add_person, update_person,
    delete_person,
)