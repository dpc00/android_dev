var set_handler = {
    set: function (obj, prop, val) {
        let oval = obj[prop];
        obj[prop] = val;
        if (val != oval && prop == "num") {
            et.dispatchEvent(new Event(obj.name + "-changed"));
        }
        return true;
    },
};

