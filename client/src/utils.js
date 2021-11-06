export function isFleetCarrier(id) {
    return id > 3700000000
}

export function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
