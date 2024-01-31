update public.block as u set
	name = u2.name,
	type = u2.type,
	description = u2.description,
	level = u2.level
from (values 
	  {data}
) as u2(id, name, type, description, level)
where u2.id = u.id;