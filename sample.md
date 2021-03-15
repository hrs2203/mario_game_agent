## Import Statement
```python3
from mario_agent import SimpleMario
```

## For training porposes 
### You don't need ui while training

```python3
train_sample_inputs = [1,2,5,3,4]
mario_env = SimpleMario()
for inp in train_sample_inputs:
    state, reward, done, info = mario_env.make_move(inp)
    print(f"current reward: {reward} ")
    if done:
        # Restart if you are dead
        mario_env.fresh_start()
## IMPORTANT: Make Sure to Close env when you are done
mario_env.close_env()
```


## For Playing Game

```python3
mario_env = SimpleMario()

mario_env = SimpleMario()
mario_env.play_game(moveCount=10)
## IMPORTANT: Make Sure to Close env when you are done
mario_env.close_env()
```
