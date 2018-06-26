' setup the video component to be chromless / ignore input (no seeking, etc)
function init()
    video = m.top.findNode("vidiot")
    video.setFocus(true)
    video.enableUI  = false
    video.enableTrickPlay = false
    video.loop = true
end function

' this gets called when the main thread gets a Remote Control API message
' telling us to play new video
function NewContent()
    print "New Content ", m.top.content
    video = m.top.findNode("vidiot")
    video.content = m.top.content
    video.control = "play"
end function
