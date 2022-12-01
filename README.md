# Postal Address Generator
Generates a file with random postal address of the region of Madrid

```python
python .\main.py -g -c 50 -s 2  .\data\ListaDeCallesDeMadrid.txt .\data\ListaDeNombresPropios.txt .\data\ListaDeApellidos.txt outpu
t.txt
```

Options:

| Parameter |                                       | 
|:---------:|---------------------------------------|
| -g        | Resolve geocoordinates of addresses   |
| -c        | Number of contacts to generate        |
| -s        | Number of surnames (default 1)        |



