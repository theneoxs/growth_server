UPDATE 
    public.status_block
SET 
    is_favorite = {is_favorite}
WHERE 
    block_id = {block_id} and user_id = '{user_id}';