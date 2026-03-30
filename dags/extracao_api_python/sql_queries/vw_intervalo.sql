create or replace view extracao_palavras_aleatorias.vw_aleatorias_ocorrencias as 
    select intervalo,
    count(*) as intervalo_entre  
    from extracao_palavras_aleatorias.gold_palavras_aleatorias
    group by intervalo