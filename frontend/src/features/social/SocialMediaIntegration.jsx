import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { getEsportsActivity, getUserData } from '../../services/socialMediaAPI';
import BlueskyConnect from './BlueskyConnect';
import BlueskyProfile from '../../components/social_account/BlueskyProfile';
import profileDataMock from './profileDataMock';

const SocialMediaIntegration = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activityData, setActivityData] = useState(null);
  const [socialAccounts, setSocialAccounts] = useState([]);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('connect'); // 'connect' ou 'activity'

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const activity = await getEsportsActivity(user._id);
        setActivityData(activity);
      } catch (err) {
        console.error('Error fetching user social accounts:', err);
      }
    };

    if (user?._id) {
      fetchUserData();
    }
  }, [user]);


  return (
    <div>
      <BlueskyProfile
        profile_data={activityData}
      />
    </div>
  );
};

export default SocialMediaIntegration;