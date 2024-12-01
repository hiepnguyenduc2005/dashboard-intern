import React from 'react';
import { Level } from './Individual/Level';
import { Metrics } from './Individual/Metrics';
import { MonthlyPoints } from './Individual/MonthlyPts';
import { SprintPoints } from './Individual/SprintPts';
import { MonthlyBreakdown } from './Individual/MonthlyTasks';
import { MonthlyTime } from './Individual/MonthlyTime';

const Individual = (props) => {
    return (
        <>
            <div className='heading'>
                <h1>Employee Peformance Dashboard</h1>
            </div>
            <div className='subhead level'>
                <Level id={props.id} status={props.status}/>
            </div>
            <div className='subhead grid4'>
                <Metrics id={props.id} status={props.status}/>
            </div>
            <div className='subhead grid2'>
                <MonthlyPoints id={props.id} status={props.status}/>
                <SprintPoints id={props.id} status={props.status}/>
            </div>
            <div className='subhead grid2'>
                <MonthlyBreakdown id={props.id} status={props.status}/>
                <MonthlyTime id={props.id} status={props.status}/>
            </div>
        </>
    )
};

export default Individual;