UPDATE public.program
	SET  name='{name}', image='{image}', description='{description}', tag='{tag}', is_public={is_public}, status={status}
	WHERE id={id};