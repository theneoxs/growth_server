SELECT 
	prog1.id, 
	prog1.name, 
	prog1.image, 
	prog1.description, 
	prog1.tag,
	prog2.count_block,
	prog2.count_success,
	prog2.count_error,
	prog2.role_id as role,
	prog2.is_favorite
FROM
	public.program prog1
	left join
	(
	SELECT 
		prog1.id,
		pl1.count_block,
		prog3.role_id,
		prog3.is_favorite,
		prog_list.count_success,
		prog_list_error.count_error
	FROM 
		public.program prog1
		left join
		(select
		 	program_id,
			count(block_id) count_block
		from
			public.program_list
		group by program_id) pl1 on pl1.program_id = prog1.id
		left join
		(
			select
				prog1.program_id,
				prog1.role_id,
				prog1.is_favorite
			from
				public.program_to_user prog1
			where
				prog1.user_id = '{user_id}'
		) prog3 on prog3.program_id = prog1.id
		left join
		(select 
		 	prog_list1.program_id,
		 	count(prog_list1.block_id) count_success
		 from
		 	public.program_list prog_list1
		 	left join public.status_block s_bl1
		 	on prog_list1.block_id = s_bl1.block_id
		 where s_bl1.user_id = '{user_id}'
		 and (s_bl1.block_status = '2' or s_bl1.block_status = '4')
		 group by prog_list1.program_id
		) prog_list on prog_list.program_id = prog1.id
		left join
		(select 
		 	prog_list1.program_id,
		 	count(prog_list1.block_id) count_error
		 from
		 	public.program_list prog_list1
		 	left join public.status_block s_bl1
		 	on prog_list1.block_id = s_bl1.block_id
		 where s_bl1.user_id = '{user_id}'
		 and (s_bl1.block_status = '3')
		 group by prog_list1.program_id
		) prog_list_error on prog_list_error.program_id = prog1.id
		) prog2 on prog1.id = prog2.id
		where 
		prog2.is_favorite = True