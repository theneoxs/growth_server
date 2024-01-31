SELECT pr1.id, pr1.name, pr1.image, pr1.description "info", pr1.tag, pr1.status
	FROM public.program as pr1
where pr1.id = {id};