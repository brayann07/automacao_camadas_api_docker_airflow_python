create or replace view extracao_palavras_aleatorias.vw_aleatorias_duplicadas as 
    select palavra, 
    count(*) as aparecimentos_nome 
    from extracao_palavras_aleatorias.gold_palavras_aleatorias
    group by palavra