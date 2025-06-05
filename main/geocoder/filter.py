all_prices = [14, 20, 21, 22, 33, 46, 47, 48, 49, 53]
indexes_to_remove = [4,7,9]

def filter_array_by_indexes(all_prices, indexes_to_remove):
    """
    Фільтрує масив, видаляючи елементи за вказаними індексами.
    
    Args:
        all_prices (list): Початковий масив з усіма значеннями.
        indexes_to_remove (list): Список індексів елементів, які потрібно видалити.
    
    Returns:
        list: Відфільтрований масив.
    """
    return [all_prices[i] for i in range(len(all_prices)) if i not in indexes_to_remove]
filtered_prices = filter_array_by_indexes(all_prices, indexes_to_remove)
print(filtered_prices)  