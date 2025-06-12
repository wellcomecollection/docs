There have been [a few different tickets](https://github.com/wellcomecollection/wellcomecollection.org/milestone/78) tackling the desired MVP logic for the [Related works component](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/content/webapp/components/RelatedWorks). There have been a lot of different conversations around what we think should be queried, and we thought it best to document it somewhere. It is likely to change and be improved upon.

[Final design and spec](https://www.figma.com/design/6ZvjrD9yhBBZSAXENc8vK4/Related-content-on-Works-pages?node-id=532-7370&p=f&m=dev)

## Related works component
The component gets added to a page if ...

## Current queries
The base of all queries lies with the subject labels. 
If a work does not have any subject labels, we don't query for the others at all.

### Subject labels

### Date range
One tab
Century
Queried if the date is a string made of four numbers. 
Valid:
- `1999`
- `1284`
- `1683`

Not valid:
- `[1928]`
- `1937?`
- `From 1930 to 1934`
- `1933-1954`

### Types/techniques
Maximum of 2 tabs