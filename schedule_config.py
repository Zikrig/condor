from datetime import time

# Конфигурация расписания
SCHEDULE_CONFIG = [
    {
        'schedule': {
            'hour': 4,
            'minute': 44,
            'day_of_week': 'mon-fri'  # Понедельник-пятница
        },
        'task_type': 'theme',
        'params': {'theme': 'content'}
    },
    {
        'schedule': {
            'hour': 7,
            'minute': 30,
            'day_of_week': '0,2,4'  # Воскресенье, вторник, четверг (0-6, где 0=воскресенье)
        },
        'task_type': 'theme',
        'params': {'theme': 'content'}
    },
    {
        'schedule': {
            'hour': 8,
            'minute': 0,
            'day_of_week': '*'  # Каждый день
        },
        'task_type': 'post_id',
        'params': {'post_id': 186}
    }
] 