import React, { useState } from 'react';

import ahk from '../ahk/ahk.json';
import WeightChart from '../components/charts/weight';

function QuantitiesGraphs() {
    const [selectedQuantity, setSelectedQuantity] = useState(null);

    let quant_list = [];
    for (let date in ahk.quantities) {
        for (let quantity in ahk.quantities[date]) {
            if (!quant_list.includes(quantity)) {
                quant_list.push(quantity);
            }
        }
    }

    // set state to first quant
    if (!selectedQuantity && quant_list.length > 0) {
        setSelectedQuantity(quant_list[0]);
    }
    
    return (
        <>
            <div>
                {quant_list.slice(0, 3).map((quantity, index) => (
                    <button key={index} onClick={() => setSelectedQuantity(quantity)}>
                        {quantity}
                    </button>
                ))}
            </div>
            {selectedQuantity && (
                <WeightChart data={ahk.quantities} quantity={selectedQuantity} />
            )}
        </>
    );
}

export default QuantitiesGraphs;