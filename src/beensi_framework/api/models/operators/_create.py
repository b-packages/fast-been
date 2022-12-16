def create(db, model, **data):
    inst = model(**data)
    inst.set_controller_fields()
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst
