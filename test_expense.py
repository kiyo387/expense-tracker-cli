import pytest
from expense import filter_by_category, next_id


def test_next_id_with_existing_expenses():
    expenses = [{"id": 1}, {"id": 2}, {"id": 5}]
    assert next_id(expenses) == 6


def test_next_id_empty_list():
    """Edge case: next_id should return 1 when given an empty list."""
    assert next_id([]) == 1


def test_filter_by_category_normal():
    expenses = [
        {"id": 1, "category": "food", "amount": 10.0},
        {"id": 2, "category": "transport", "amount": 20.0},
        {"id": 3, "category": "food", "amount": 15.0},
    ]
    result = filter_by_category(expenses, "food")
    assert len(result) == 2
    assert [e["id"] for e in result] == [1, 3]


def test_filter_by_category_mixed_case():
    """Edge case: filter_by_category should handle mixed-case categories."""
    expenses = [
        {"id": 1, "category": "food", "amount": 10.0},
        {"id": 2, "category": "Food", "amount": 12.0},
        {"id": 3, "category": "transport", "amount": 20.0},
    ]
    result_upper = filter_by_category(expenses, "FOOD")
    result_mixed = filter_by_category(expenses, "fOoD")
    result_spaced = filter_by_category(expenses, "  Food  ")

    assert len(result_upper) == 2
    assert len(result_mixed) == 2
    assert len(result_spaced) == 2
    assert [e["id"] for e in result_upper] == [1, 2]


def test_filter_by_category_empty_list():
    """Edge case: filter_by_category should return an empty list when given an empty list."""
    assert filter_by_category([], "food") == []


def test_filter_by_category_no_match():
    expenses = [{"id": 1, "category": "food"}]
    assert filter_by_category(expenses, "entertainment") == []
