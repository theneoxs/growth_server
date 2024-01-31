UPDATE 
    public.program_to_user
SET 
    is_favorite = {is_favorite}
WHERE 
    program_id = {program_id} and user_id = '{user_id}';