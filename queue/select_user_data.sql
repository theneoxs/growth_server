select 
	usr1.id,
	usr1.name,
	usr1.surname,
	usr1.position,
	role1.id role_id,
	role1.name role_name,
	branch1.name branch_name
from
	public.user usr1
	left join 
		public.role role1
	on
		usr1.role_id = role1.id
	left join 
		public.branch branch1
	on
		usr1.branch_id = branch1.id
where
	usr1.id = '{user_id}'