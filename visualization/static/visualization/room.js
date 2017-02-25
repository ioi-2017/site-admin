/**
 * Created by hamed on 2/21/17.
 */

function getRoom(container) {
    return Raphael(container.attr("id"), "100%", "100%");
}

function getContainer(room) {
    return room.canvas.parentElement;
}

function createDesk(room, x, y, angle) {
    var parent = getContainer(room);
    var absX = parent.offsetWidth * x, absY = parent.offsetHeight * y;
    var deskWidth = 40, deskHeight = 20;
    var desk = room.rect(absX - deskWidth / 2, absY - deskHeight / 2, deskWidth, deskHeight, 2);
    desk.rotate(angle);
    desk.attr("fill", "#f00");
    desk.attr("stroke", "#faa");
    return desk;
}