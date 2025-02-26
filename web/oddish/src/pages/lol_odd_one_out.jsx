import React from 'react'

import kits from '../lol/exported_kits.json';

console.log(kits);

function LolSkill({ skill }) {

    let passive = skill.includes('_P');
    let group = passive ? 'passive' : 'spell';


    return (
        <>
            <img src={`https://ddragon.leagueoflegends.com/cdn/15.4.1/img/${group}/${skill}`} />
            <p>{skill.name}</p>
        </>
    )
}


function LOLOddOneOut() {

  return (
    <>
        <LolSkill skill='Aatrox_P.png' />
        <LolSkill skill='Aatrox_Q.png' />
        <LolSkill skill='Aatrox_W.png' />
        <LolSkill skill='Aatrox_E.png' />
        <LolSkill skill='Aatrox_R.png' />
    </>

  )
}

export default LOLOddOneOut


