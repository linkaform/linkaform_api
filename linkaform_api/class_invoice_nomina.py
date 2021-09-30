from typing import Dict, List, Optional, Union
from pydantic import BaseModel

class ComplementData(BaseModel):
    # Complementos de la Nomina
    tipo_nomina: Optional[str]
    fecha_pago: Optional[str]
    fecha_inicial_pago: str
    fecha_final_pago: str
    num_dias_pagados: float
    emisor: Optional[Dict]
    receptor: Dict
    percepciones: Optional[Dict]
    deducciones: Optional[List[Dict]]
    otros_pagos: Optional[List[Dict]]
    incapacidades: Optional[List[Dict]]

class InvoiceComplement(BaseModel):
    type: str
    data: ComplementData

class InvoiceNomina(BaseModel):
    type: str
    customer: Union[str, Dict]
    folio_number: Optional[int]
    series: Optional[str]
    date: Optional[str]
    complements: List[InvoiceComplement]
    external_id: Optional[str]