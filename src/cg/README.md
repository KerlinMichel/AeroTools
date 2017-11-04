# Center of Gravity Tool

## Run script

```sh
python cg.py
```

### Usage

Load in objects from csv file
```sh
(cg-tool) load [filename]
```

Example file:
```
name,x,y,z,weight
plane,0,1.5,5,15
electronics,0,1.75,6,3
```

Calculate the cg of the current object
```sh
(cg-tool) cg
```

Adjust the cg of the current object by adding a new object

```sh
(cg-tool) adjust_cg_with_obj [new_object weight] [desired cg_x] [desired cg_y] [desired cg_z]
```
