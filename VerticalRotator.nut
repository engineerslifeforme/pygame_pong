///////////////////////////////////////////////////
//
// Attract-Mode Frontend - VerticalRotator plugin
//
///////////////////////////////////////////////////
//
// Define the user-configurable options:
//
class UserConfig </ help="Plugin to select display by touching specific cab controls (i.e. 3 sided cocktail tables) " /> {

	</ label="Horizontal Up control", help="The input to press for 'up'", is_input=true, order=3 />
	hup="";

	</ label="Horizontal Down control", help="The input to press for 'down'", is_input=true, order=4 />
	hdown="";

	</ label="Horizontal Left control", help="The input to press for 'left'", is_input=true, order=5 />
	hleft="";

	</ label="Horizontal Right control", help="The input to press for 'right'", is_input=true, order=6 />
	hright="";

	</ label="Horizontal A button", help="The input to press for 'A'", is_input=true, order=7 />
	hA="";

	</ label="Horizontal B button", help="The input to press for 'B'", is_input=true, order=8 />
	hB="";

	</ label="Horizontal C button", help="The input to press for 'C'", is_input=true, order=9 />
	hC="";

        </ label="Vertical Up control", help="The input to press for 'up'", is_input=true, order=13 />
	vup="";

	</ label="Vertical Down control", help="The input to press for 'down'", is_input=true, order=14 />
	vdown="";

	</ label="Vertical Left control", help="The input to press for 'left'", is_input=true, order=15 />
	vleft="";

	</ label="Vertical Right control", help="The input to press for 'right'", is_input=true, order=16 />
	vright="";

	</ label="Vertical A button", help="The input to press for 'A'", is_input=true, order=17 />
	vA="";

	</ label="Vertical B button", help="The input to press for 'B'", is_input=true, order=18 />
	vB="";

	</ label="Vertical C button", help="The input to press for 'C'", is_input=true, order=19 />
	vC="";

	</ label="Display Vertical", help="Display name for vertical layout", order=20 />
	vDisp="";

	</ label="Display Horizontal", help="Display name for horizontal layout", order=21 />
	hDisp="";

}

class VerticalRotator
{
	m_config = null;

	m_current = 0;
	m_horizontal = [ "hup", "hdown", "hright", "hleft", "hA", "hB", "hC" ];
	m_vertical = [ "vup", "vdown", "vright", "vleft", "vA", "vB", "vC" ];

	constructor()
	{
		m_config = fe.get_config();
		fe.add_ticks_callback( this, "on_tick" );
		fe.add_transition_callback( this, "on_transition" )	
	}

	function load_display_name(name) 
	{
  		foreach( idx, display in fe.displays )
      			if ( name == fe.displays[idx].name && name != fe.displays[fe.list.display_index].name )
				fe.set_display(idx)
	}

	function on_tick( ttime )
	{
		if ( fe.overlay.is_up )
			return;
		
		if ( m_current == 0 )  // In horizontal layout, check for vertical keys
		{
			foreach ( v in m_vertical )
			{
				local down = fe.get_input_state( m_config[ v ] );
				if ( down )
				{
					//fe.layout.base_rotation = RotateScreen.Right;
					load_display_name(m_config["vDisp"]);
					m_current = 1;
					break;
				}
			}
		} 
		else
		{
			foreach ( v in m_horizontal )
			{
				local down = fe.get_input_state( m_config[ v ] );
				if ( down )
				{
					//fe.layout.base_rotation = RotateScreen.None;
					load_display_name(m_config["hDisp"]);
					m_current = 0;
					break;
				}
			}
		}
	}

	function on_transition( ttype, var, ttime )
	{
		if ( ttype == Transition.StartLayout )
		{
			if ( fe.nv.rawin( "VerticalRotator" ) )
			{
				m_current = fe.nv[ "VerticalRotator" ];
				delete fe.nv[ "VerticalRotator" ];
			}
		}
		else if (( ttype == Transition.EndLayout )
			&& ( m_current > 0 ))
		{
			fe.nv[ "VerticalRotator" ] <- m_current;
		}
	}
}

// Create an entry in the fe.plugin table in case anyone else wants to
// find this plugin.
//
if ( !ScreenSaverActive )
	fe.plugin[ "VerticalRotator" ] <- VerticalRotator();
